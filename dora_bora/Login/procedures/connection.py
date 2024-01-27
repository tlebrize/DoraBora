import random
import string

from django.conf import settings
from django.contrib.auth.hashers import acheck_password

from Login.ank_crypto import ank_decrypt
from Login.models import Account, Server


def make_key():
    return "".join(random.choices(string.ascii_lowercase, k=32))


async def send_policy(s):
    await s.write(
        """
<?xml version="1.0" encoding="UTF-8"?>
<cross-domain-policy>
<site-control permitted-cross-domain-policies="all"/>
<allow-access-from domain="*" to-ports="*" secure="false"/>
<allow-http-request-headers-from domain="*" headers="*" secure="false"/>
</cross-domain-policy>"
""".strip()
    )


async def send_key(s):
    assert s.key

    await s.write(f"HC{s.key}", drain=True)


async def check_version(s):
    given = await s.readline()
    if given != settings.CLIENT_VERSION:
        raise Exception(f"Invalid version : `{given}`.")


async def switch_login(s):
    switch_token = (await s.readline())[:196]

    try:
        s.account = await Account.objects.aget(switch_token=switch_token)
    except Account.DoesNotExist:
        raise Exception("Invalid switch_token")

    s.account.switch_token = None
    await s.account.asave()


async def password_login(s):
    assert s.key

    ank_password = await s.readline()
    check, ank_password = ank_password.split("#1")
    if check != "":
        raise Exception("Invalid password format")

    password = ank_decrypt(ank_password, s.key)

    account = await Account.objects.aget(username=s.username)
    if await acheck_password(password, account.password):
        s.account = account
    else:
        raise Exception("Invalid password.")


async def send_connected_infos(s):
    assert s.account

    server_login_list = await Server.objects.aformat_login_list()

    login_packets = [
        f"Ad{s.account.nickname}",
        f"Ac{s.account.community}",
        f"AH{server_login_list}",
        f"AlK{s.account.format_is_game_master()}",
        f"AQ{s.account.format_security_question()}",
    ]
    await s.write("\0".join(login_packets))
