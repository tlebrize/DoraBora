async def disconnect(service):
    await service.write(f"HS{service.management.account.switch_token}")
