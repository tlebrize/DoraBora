from collections import defaultdict

from Game.models import Character, Map, Monster

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
        RED = 1
        BLUE = 0

    class States:
        INIT = 1
        PLACEMENT = 2
        ONGOING = 3
        FINISHED = 4

    class FightKinds:
        MONSTER = 4

    def __init__(self, map_id, kind):
        self.id = None
        self.map_id = map_id
        self.kind = kind
        self.initiative = defaultdict(list)
        self.state = self.States.INIT
        self.teams = [[], []]
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


class Fighter:
    def __init__(self, origin, team, server=None):
        self.id = None
        self.team = team
        self.origin = origin
        self.server = server
        for stat_name in FIGHTING_STATS:
            setattr(self, stat_name, getattr(self.origin, stat_name))


async def create_monster_fight(server, group_id):
    character = await Character.objects.aget(id=server.character.id)
    fight = Fight(server.map.id, Fight.FightKinds.MONSTER)
    fight.add_fighter(
        Fighter(
            origin=character,
            team=Fight.Teams.BLUE,
            server=server,
        ),
    )
    async for monster in Monster.objects.filter(group_id=group_id):
        fight.add_fighter(Fighter(origin=monster, team=Fight.Teams.RED, server=None))
    return fight
