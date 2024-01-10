from service.shared_state import remove_character_from_map


async def disconnect(s):
    await remove_character_from_map(
        s,
        s.management.current_map.id,
        s.management.current_character.id,
    ),
    await s.write(f"HS{s.management.account.switch_token}")
