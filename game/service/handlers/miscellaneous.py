from service.shared_state import remove_character_from_map
from service.datamodel.account import AccountState


async def disconnect(s, switch=False):
    await remove_character_from_map(s)
    await s.management.set_account_state(AccountState.OFFLINE.value)
    if switch:
        await s.write(f"HS{s.management.account.switch_token}")
