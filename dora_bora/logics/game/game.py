from dora_bora.logics.exceptions import NotHandled
from dora_bora.datamodel import AccountState, Gender, Class
from .child import ChildLogic


class GameLogic(ChildLogic):
    def handle_input(self, message):
        if message.startswith("C"):
            return self.send_game_create(message[1:])
        elif message.startswith("I"):
            return self.send_extra_informations()
        raise NotHandled(message)

    def send_game_create(self, data):
        c = self.root.character
        self.outputs.put(f"GCK|1|{c.name}")
        if False:  # alignments != -1 (neutral)
            alignement = "~-1,0,0,0,0"
            # ~alignement?,alevel,arank(grade),honor,dishonor,showWings
        else:
            alignement = ""

        As = (
            f"As{c.experience},0,1000"  # current exp,current level exp,next level exp
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

        self.outputs.put(As)
        self.outputs.put(c.format_pods())
        self.inputs.put("GI")

    def send_extra_informations(self):
        if not getattr(self.root, "map"):
            self.root.map = self.db.maps.get(self.root.character.map_id)

        characters = self.shared.characters_at_map.get(self.root.map.id, [])
        for character_id in characters:
            c = self.db.characters.get(character_id)
            self.outputs.put(
                ";".join(
                    map(
                        str,
                        [
                            "GM|+210",  # cellid
                            1,  # orientation
                            0,  # ? level ?
                            c.id,
                            c.name,
                            c.class_,
                            f"{c.get_gfxid()}^100x100",  # gfxid^size
                            c.gender,
                            f"",  # -1,0,0,0
                            # alignement,?,wings,grade
                            *c.get_colors(),
                            ",,,,",  # equipment
                            "",  # Emote
                            "",  # Emote Timer
                            "",  # Guild Name
                            "",  # Guild Emblem
                            "",  # ?
                            8,  # Speed
                            "",  # Close
                        ],
                    )
                )
            )

        # mobs
        # npcs
        # perco
        # map objects? GAME_SEND_MAP_OBJECTS_GDS_PACKETS
        self.outputs.put("GDK")  # gdk ?
        self.outputs.put("fC0")  # fight counts
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
