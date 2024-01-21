from Game.ank_encodings import ank_decode_cell, ank_encode_cell
from Game.game_actions import GameActions


async def send_game_create(s, _unused):
    assert s.character
    assert s.map

    s.exchange.character_joined_map(s.character, s.map)

    await s.write(f"GCK|1|{s.character.name}")
    if False:  # alignments != -1 (neutral)
        alignement = "~-1,0,0,0,0"
        # ~alignement?,alevel,arank(grade),honor,dishonor,showWings
    else:
        alignement = ""

    await s.write(
        f"As{s.character.experience},0,1000"  # current,currentLevelExp,nextLevelExp
        "1,1,1"  # ???
        f"|{s.character.kamas}|{s.character.stat_points}|{s.character.spell_points}|"
        f"-1{alignement}|"
        "55,55|"  # hp,hpmax|
        "9999,10000|"  # energy,energymax|
        "12|"  # initiative
        "100|"  # prospection total
        # Base,Equipment,Gifts,Buffs,Total
        "6,0,0,0,6|"  # Action Points
        "3,0,0,0,3|"  # Movement Points
        # Base,Equipment,Gifts,Buffs
        "0,0,0,0|"  # strength
        "55,0,0,0|"  # vitality
        "0,0,0,0|"  # wisdom
        "0,0,0,0|"  # luck
        "0,0,0,0|"  # agility
        "0,0,0,0|"  # intelligence
        "0,0,0,0|"  # Range
        "1,0,0,0|"  # Summons
        "0,0,0,0|"  # DOMA
        "0,0,0,0|"  # PDOM
        "0,0,0,0|"  # MAITRISE
        "0,0,0,0|"  # PERDOM
        "0,0,0,0|"  # SOIN
        "0,0,0,0|"  # TRAPDOM
        "0,0,0,0|"  # TRAPPER
        "0,0,0,0|"  # RETDOM
        "0,0,0,0|"  # CC
        "0,0,0,0|"  # EC
        # Base,Equipment,0?,Buffs,Buffs
        "0,0,0,0,0|"  # AFLEE
        "0,0,0,0,0|"  # MFLEE
        "0,0,0,0,0|"  # R_NEU
        "0,0,0,0,0|"  # RP_NEU
        "0,0,0,0,0|"  # R_PVP_NEU
        "0,0,0,0,0|"  # RP_PVP_NEU
        "0,0,0,0,0|"  # R_TER
        "0,0,0,0,0|"  # RP_TER
        "0,0,0,0,0|"  # R_PVP_TER
        "0,0,0,0,0|"  # RP_PVP_TER
        "0,0,0,0,0|"  # R_EAU
        "0,0,0,0,0|"  # RP_EAU
        "0,0,0,0,0|"  # R_PVP_EAU
        "0,0,0,0,0|"  # RP_PVP_EAU
        "0,0,0,0,0|"  # R_AIR
        "0,0,0,0,0|"  # RP_AIR
        "0,0,0,0,0|"  # R_PVP_AIR
        "0,0,0,0,0|"  # RP_PVP_AIR
        "0,0,0,0,0|"  # R_FEU
        "0,0,0,0,0|"  # RP_FEU
        "0,0,0,0,0|"  # R_PVP_FEU
        "0,0,0,0,0|"  # RP_PVP_FEU
    )

    await s.write(s.character.format_pods())
    await send_extra_informations(s)


async def send_extra_informations(s):
    assert s.server
    assert s.character
    assert s.map

    await s.exchange.broadcast_map_update(s.map)

    # map gms ?
    # cases.stream().filter(cell -> cell != null).forEach(cell -> cell.getPlayers().stream().filter(player ->
    #     player != null).forEach(player -> packet.append("GM|+").append(player.parseToGM()).append('\u0000')));

    # mobs
    # npcs
    # perco
    # map objects? GAME_SEND_MAP_OBJECTS_GDS_PACKETS
    await s.write("GDK")  # gdk ?

    await s.write("fC0")  # fight counts
    # prisms
    # merchants
    # fights
    # mount parks
    # objects again ? GAME_SEND_GDO_OBJECT_TO_MAP
    # mount
    # floor items
    # interactive doors
    # prisms
    # players + jobs ?


async def handle_move_action(s, data):
    destination = ank_decode_cell(data[-2:])
    game_action_id = await s.exchange.ga_move(s.character, destination)

    current_cell_code = ank_encode_cell(s.character.map_cell_id)

    path = current_cell_code + data  # check pathfinding?
    await s.exchange.broadcast_move_action(game_action_id, s.character.id, s.map.id, path)


async def handle_action(s, data):
    action_id = int(data[:3])
    if action_id == 1:
        await handle_move_action(s, data[3:])
    else:
        raise Exception(f"Unknown action : {data}.")


async def handle_acknowledge(s, data):
    success = data[0] == "K"
    id_, *payload = data[1:].split("|")
    action_data = s.exchange.pop_action(int(id_))

    print(f"* GA : {action_data}")

    if action_data["kind"] == GameActions.MOVE:
        if success:
            s.character.map_cell_id = action_data["destination"]
        else:
            s.character.map_cell_id = int(payload[0])
        await s.character.asave()

        await s.write("BN")
    else:
        raise Exception("Unknown action : " + action_data)


async def game_handler(s, command):
    match command[0]:
        case "C":
            await send_game_create(s, command[1:])
        case "I":
            await send_extra_informations(s)
        case "A":
            await handle_action(s, command[1:])
        case "K":
            await handle_acknowledge(s, command[1:])
