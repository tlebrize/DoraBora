import random
from collections import defaultdict

from Game.ank_encodings import ank_decode_places
from Game.models import Character, Map, MonsterGroup

FIGHTING_STATS = [
    "current_hit_points",
    "max_hit_points",
    "action_points",
    "movement_points",
    "neutral_resistance",
    "earth_resistance",
    "fire_resistance",
    "water_resistance",
    "air_resistance",
    "action_points_dodge",
    "movement_points_dodge",
    "strength",
    "wisdom",
    "inteligence",
    "luck",
    "agility",
]


class Fight:
    class Teams:
        RED = 0
        BLUE = 1

    class States:
        INIT = 1
        PLACEMENT = 2
        ONGOING = 3
        FINISHED = 4

    class Kinds:
        MONSTER = 4

    def __init__(self, map_id, kind):
        self.id = None
        self.map_id = map_id
        self.kind = kind
        self.initiative = defaultdict(list)
        self.state = self.States.INIT
        self.teams = {
            self.Teams.BLUE: [],
            self.Teams.RED: [],  # in PvM it is assumed that red is the players team.
        }
        self.servers = []
        self.places = None

        self.lobby_time_left = 45

    def add_fighter(self, fighter):
        self.teams[fighter.team].append(fighter)
        self.servers.append(fighter.server)

    def format_gjk(self):
        cancelable = int(self.kind in [])
        duel = 1
        spec = 1
        return f"GJK{self.state}|{cancelable}|{duel}|{spec}|{self.lobby_time_left * 1000}|{self.kind}"

    async def format_gdf(self):
        pass  # TODO : GAME_SEND_GDF_PACKET_TO_FIGHT

    async def format_gp(self, team):
        if not self.places:
            self.places = (await Map.objects.aget(id=self.map_id)).places
        return f"GP{self.places[0]}|{self.places[1]}|{team}"

    async def format_gc(self):
        # flags
        if self.kind == Fight.Kinds.MONSTER:
            character = self.teams[Fight.Teams.RED][0].origin
            group = self.teams[Fight.Teams.BLUE][0].group

            return "Gc+" + "|".join(
                [
                    f"{character.id};{self.kind}",  # dunno why character.id twice ?
                    f"{character.id};{character.cell_id};0;-1",
                    f"{group.id};{group.cell_id};1;-1",
                    # dunno what 1 0 and -1 mean ?
                ]
            )

    async def set_ready(self, fighter, ready):
        fighter.ready = ready
        # self.check_ready()
        await fighter.server.exchange.broadcast_to_fight(f"GR{int(ready)}{fighter.origin.id}", self)

    async def change_placement(self, fighter, cell_id):
        fighter.cell_id = cell_id
        # TODO check already occupied
        await fighter.server.exchange.broadcast_to_fight(f"GIC|{fighter.origin.id};{cell_id};1", self)


class Fighter:
    class Kinds:
        MONSTER = 1
        CHARACTER = 2

    def __init__(self, kind, origin, team, cell_id, server=None, group=None, ready=False):
        self.kind = kind
        self.team = team
        self.origin = origin
        self.cell_id = cell_id
        self.server = server
        self.group = group
        self.ready = ready
        for stat_name in FIGHTING_STATS:
            setattr(self, stat_name, getattr(self.origin, stat_name))

    def format_gt(self):
        return f"Gt{self.team}|+{self.origin.format_gt()}"

    def format_gm(self):
        return self.origin.format_fight_gm(self.team, self.cell_id)


async def create_monster_fight(server, group_id):
    character = await Character.objects.aget(id=server.character.id)
    cells = ank_decode_places(server.map)
    fight = Fight(server.map.id, Fight.Kinds.MONSTER)
    fighter = Fighter(
        kind=Fighter.Kinds.CHARACTER,
        origin=character,
        team=Fight.Teams.RED,
        cell_id=random.choice(cells[Fight.Teams.RED])["cell_id"],
        server=server,
    )
    fight.add_fighter(fighter)
    group = await MonsterGroup.objects.aget(id=group_id)
    monster_cells = cells[Fight.Teams.BLUE]
    async for monster in group.monsters.all():
        cell = monster_cells.pop(random.randint(0, len(monster_cells) - 1))
        fight.add_fighter(
            Fighter(
                kind=Fighter.Kinds.MONSTER,
                origin=monster,
                team=Fight.Teams.BLUE,
                cell_id=cell["cell_id"],
                group=group,
                ready=True,
            )
        )
    return fight, fighter
