from Login.models import Account


async def disconnect(s):
    assert s.account

    if s.map:
        s.exchange.character_left_map(s.character, s.map)
        await s.exchange.broadcast_map_update(s.map)

    if s.character:
        s.exchange.character_disconnected(s.character)

    s.account.state = Account.States.OFFLINE


async def disconnect_switch(s):
    assert s.account

    await disconnect(s)
    await s.write(f"HS{s.account.switch_token}")
