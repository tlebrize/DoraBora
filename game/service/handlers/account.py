async def connect(service, data):
        account = await service.management.get_account_by_id(int(data))
        if account.state != AccountState.IN_LOGIN:
            raise Exception("Account not in login.")

        await asyncio.gather(
            service.write('ATK0'),
            service.management.set_account_state(AccountState.IN_GAME),
        )

async def account_handler(service, command):
    case command[0]:
        match 'T':
            await connect(service, command[1:])
