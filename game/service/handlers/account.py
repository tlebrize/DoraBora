import asyncio
from service.datamodel import AccountState, Gender, Class
from service.exchange import create_exchange_task
from service.shared_state import add_character_to_map


async def connect(service, data):
    account = await service.management.get_account_by_id(int(data))
    if account.state != AccountState.IN_LOGIN.value:
        print(str(account.state), str(AccountState.IN_LOGIN.value))
        raise Exception("Account not in login.")

    await asyncio.gather(
        service.write("ATK0"),
        service.management.set_account_state(AccountState.IN_GAME.value),
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
    await service.write(f"Af1|1|1|1|{service.server_id}")


async def join_game(s, character_id):
    c = await s.management.set_current_character(character_id)
    current_map = await s.management.get_current_map(c.map)
    await add_character_to_map(s, current_map.id, c.id)

    # check seller ?
    # check mount
    await s.write("Rx0")  # mount exp
    await s.write(
        f"ASK|{c.id}|{c.name}|{c.level}|{c._class}|{c.gender}|"
        f"{c.get_gfxid()}" + "|".join(map(str, c.get_colors())) + "|"
        # Items
    )
    # check fight
    await s.write("ILS2000")  # No fight
    # check jobs
    await s.write("ZS-1")  # Alignment neutral
    await s.write("cC+i*")  # chats enabled
    # check guild
    await s.write("al|")  # Zone alignment
    await s.write("eL0|0")  # Emotes
    await s.write("AR6bk")  # Restrictions
    await s.write(c.format_pods())  # used_pods|max_pods
    await s.write(current_map.format_map_data())
    # self.shared.characters.move_to_map(c.id, self.root.map.id)
    # self.shared.characters.move_to_cell(c.id, 210)
    await s.write("fC0")  # fight counts
    await s.write("FO-")  # - = don't see friend connection / +
    await s.write("SL1~1~1;2~1~2;3~2~4;")  # Spell list id~level~placement;
    await s.write("Im189")  # Welcome message, non-existant
    await s.write("Im0153;127.0.0.1")  # IP msg
    await s.create_server_exchange()
    await s.broadcast(f"server.{s.server_id}", "Hello")


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


async def delete_character(service, data):
    id_, _ = data.split("|")
    if int(id_) in [c.id for c in service.management.character_list.characters]:
        await service.management.delete_character(id_)
        await send_character_list(service)
    else:
        await service.write("ADE")


async def account_handler(service, command):
    match command[0]:
        case "A":
            await create_character(service, command[1:])
        case "D":
            await delete_character(service, command[1:])
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
