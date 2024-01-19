from Login.models import Account, Server


async def send_server_list(s):
    assert s.account

    await s.write("AxK" + s.account.format_subscribed() + await Server.objects.format_server_list(s.account.id))


async def handle_server_connection(s, server_id):
    assert s.account

    try:
        server = await Server.objects.aget(id=server_id)
    except Server.DoesNotExist as exc:
        raise Exception(f"server not found {server_id}") from exc

    s.account.state = Account.States.IN_LOGIN
    await s.account.asave()

    await s.write(f"AYK{server.format_connection()};{s.account.id}")


async def handle_switch_token(s, token):
    assert s.account

    # unsure about what this really does.
    s.account.switch_token = token[:196]
    await s.account.asave()
