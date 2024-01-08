import asyncio
from service.datamodel import AccountState, Gender, Class


async def connect(service, data):
    account = await service.management.get_account_by_id(int(data))
    if account.state != AccountState.IN_LOGIN:
        raise Exception("Account not in login.")

    await asyncio.gather(
        service.write("ATK0"),
        service.management.set_account_state(AccountState.IN_GAME),
    )


async def set_key_index(_, key_index):  # Unused
    print(key_index)


async def send_region_version(service):  # Unused
    await service.write(f"AV0")


async def set_language(_, lang_code):  # Unused
    print(lang_code)


async def send_character_list(service):
    characters = await service.management.list_characters()

    await service.write(
        "ALK"
        + "|".join(
            map(
                str,
                [
                    service.management.account.subscribed_milliseconds(),
                    characters.count(),
                    characters.format_alk(),
                ],
            )
        )
    )


async def send_queue_position(service):  # Disabled
    await service.write(f"Af1|1|1|1|{service.management.server_id}")


async def join_game(service, character_id):
    c = await service.management.set_current_character(character_id)
    current_map = await service.management.set_current_map(c.map)

    # check seller ?
    # check mount
    await service.write("Rx0")  # mount exp
    await service.write(
        f"ASK|{c.id}|{c.name}|{c.level}|{c._class}|{c.gender}|"
        f"{c.get_gfxid()}" + "|".join(map(str, c.get_colors())) + "|"
        # Items
    )
    # check fight
    await service.write("ILS2000")  # No fight
    # check jobs
    await service.write("ZS-1")  # Alignment neutral
    await service.write("cC+i*")  # chats enabled
    # check guild
    await service.write("al|")  # Zone alignment
    await service.write("eL0|0")  # Emotes
    await service.write("AR6bk")  # Restrictions
    await service.write(c.format_pods())  # used_pods|max_pods
    await service.write(current_map.format_map_data())
    # self.shared.characters.move_to_map(c.id, self.root.map.id)
    # self.shared.characters.move_to_cell(c.id, 210)
    await service.write("fC0")  # fight counts
    await service.write("FO-")  # - = don't see friend connection / +
    await service.write("SL1~1~1;2~1~2;3~2~4;")  # Spell list id~level~placement;
    await service.write("Im189")  # Welcome message, non-existant
    await service.write("Im0153;127.0.0.1")  # IP msg


async def create_character(service, data):
    name, _class, gender, c1, c2, c3 = data.split("|")
    await service.management.create_character(
        name=name,
        gender=Gender(int(gender)),
        _class=Class(int(_class)),
        colors=[int(c1), int(c2), int(c3)],
    )
    await service.write("AAK")  # create perso ok
    await send_character_list(service)


async def account_handler(service, command):
    match command[0]:
        case "A":
            await create_character(service, command[1:])
        case "T":
            await connect(service, command[1:])
        case "k":
            await set_key_index(service, int(command[1:]))
        case "V":
            await send_region_version(service)
        case "g":
            await set_language(service, command[1:])
        case "L":
            await send_character_list(service)
        case "f":
            await send_queue_position(service)
        case "S":
            await join_game(service, int(command[1:]))
