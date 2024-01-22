import asyncio

from Game.models import Character, Map
from Login.models import Account


async def create_character(s, data):
    assert s.account

    name, _class, gender, c1, c2, c3 = data.split("|")
    await Character.objects.acreate(
        server=s.server,
        account=s.account,
        name=name,
        gender=Character.Gender(int(gender)),
        _class=Character.Class(int(_class)),
        colors=[int(c1), int(c2), int(c3)],
    )

    await s.write("AAK")
    await send_character_list(s)


async def delete_character(s, data):
    assert s.account

    id_, _ = data.split("|")

    if await Character.objects.filter(id=id_).adelete():
        await send_character_list(s)
    else:
        await s.write("ADE")


async def connect(s, data):
    s.account = await Account.objects.aget(id=int(data))

    if s.account.state != Account.States.IN_LOGIN:
        raise Exception("Account not in login.")

    s.account.state = Account.States.IN_GAME

    await asyncio.gather(
        s.write("ATK0"),
        s.account.asave(),
    )


async def set_key_index(_, key_index):  # Unused
    pass


async def send_region_version(s):  # ???
    await s.write(f"AV0")


async def set_language(_, lang_code):  # Unused
    pass


async def send_character_list(s):
    assert s.account

    characters = Character.objects.filter(account_id=s.account.id, server_id=s.server.id)

    await s.write(
        "ALK"
        + "|".join(
            map(
                str,
                [
                    s.account.subscribed_milliseconds(),
                    await characters.acount(),
                    await characters.format_alk(),
                ],
            )
        )
    )


async def send_queue_position(s):  # Disabled
    await s.write(f"Af1|1|1|1|{s.server.id}")


async def join_game(s, character_id):
    assert s.account

    s.character = await Character.objects.aget(account_id=s.account.id, id=character_id)
    s.exchange.character_connected(s.character, s)
    s.map = await Map.objects.aget(id=s.character._map_id)

    # check seller ?
    # check mount
    await s.write("Rx0")  # mount exp
    await s.write(
        f"ASK|{s.character.id}|{s.character.name}|{s.character.level}|{s.character._class}|{s.character.gender}|"
        f"{s.character.get_gfxid()}" + "|".join(map(str, s.character.get_colors())) + "|"
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
    await s.write(s.character.format_pods())  # used_pods|max_pods
    await s.write(s.map.format_GDM())
    # self.shared.characters.move_to_map(c.id, self.root.map.id)
    # self.shared.characters.move_to_cell(c.id, 210)
    await s.write("fC0")  # fight counts
    await s.write("FO-")  # - = don't see friend connection / +
    await s.write("SL1~1~1;2~1~2;3~2~4;")  # Spell list id~level~placement;
    await s.write("Im189")  # Welcome message, non-existant
    await s.write("Im0153;127.0.0.1")  # IP msg
    # await s.create_server_exchange()
    # await s.broadcast(f"server.{s.server.id}", "Hello")


async def account_handler(s, command):
    match command[0]:
        case "A":
            await create_character(s, command[1:])
        case "D":
            await delete_character(s, command[1:])
        case "T":
            await connect(s, command[1:])
        case "k":
            await set_key_index(s, int(command[1:]))
        case "V":
            await send_region_version(s)
        case "g":
            await set_language(s, command[1:])
        case "L":
            await send_character_list(s)
        case "f":
            await send_queue_position(s)
        case "S":
            await join_game(s, int(command[1:]))
