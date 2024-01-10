from service.shared_state import list_characters_on_map


async def send_game_create(service, _unused):
    c = service.management.current_character
    await service.write(f"GCK|1|{c.name}")
    if False:  # alignments != -1 (neutral)
        alignement = "~-1,0,0,0,0"
        # ~alignement?,alevel,arank(grade),honor,dishonor,showWings
    else:
        alignement = ""

    await service.write(
        f"As{c.experience},0,1000"  # current,currentLevelExp,nextLevelExp
        "1,1,1"  # ???
        f"|{c.kamas}|{c.stat_points}|{c.spell_points}|"
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

    await service.write(c.format_pods())
    await send_extra_informations(service)


async def send_extra_informations(s):
    # if not getattr(self.root, "map"):
    #     self.root.map = self.db.maps.get(self.root.character.map_id)

    # characters = self.shared.maps.characters.get(self.root.map.id, [])

    # clients = self.shared.maps.list_clients_on_map(self.root.map.id)
    # for client in clients:
    #     if client:
    #         for character_id in characters:
    #             client.outputs.put(
    #                 game.GM(
    #                     self.db.characters.get(character_id),
    #                     self.shared.characters.get_cell(character_id),
    #                 )
    #             )
    #             client.flush()

    print(await list_characters_on_map(s, s.management.current_map.id))

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


async def game_handler(service, command):
    match command[0]:
        case "C":
            await send_game_create(service, command[1:])
        case "I":
            print("pls")
            await send_extra_informations(service)
