from Login.models import Account


async def disconnect(s):
    assert s.account

    # await remove_character_from_map(s)
    s.account.state = Account.States.OFFLINE


async def disconnect_switch(s):
    assert s.account

    await disconnect(s)
    await s.write(f"HS{s.account.switch_token}")
