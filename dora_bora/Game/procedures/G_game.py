from asgiref.sync import sync_to_async

from .GA_game_actions import handle_game_action
from .GK_game_action_acknoledges import handle_game_action_acknowledges


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

    monster_gms = await sync_to_async(s.map.format_monster_groups_GM)()
    if monster_gms:
        await s.write(f"GM|{monster_gms}")

    # npcs
    # perco
    await s.write(f"GDF{s.map.format_GDF()}")

    await s.write("GDK")  # gdk ?

    await s.write("fC0")  # fight counts
    # prisms
    # merchants
    # fights
    # mount parks
    # mount park objects
    # mount
    # floor items
    # interactive doors
    # prisms
    # players + jobs ?


async def game_handler(s, command):
    match command[0]:
        case "C":
            await send_game_create(s, command[1:])
        case "I":
            await send_extra_informations(s)
        case "A":
            await handle_game_action(s, command[1:])
        case "K":
            await handle_game_action_acknowledges(s, command[1:])
