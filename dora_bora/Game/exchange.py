import asyncio
from collections import defaultdict

from DoraBora.counter import AsyncCounter
from Game.game_actions import GameActions


class Exchange:
    def __init__(self):
        self.client_counter = AsyncCounter()

        self.characters_server = {}
        self.characters_on_maps = defaultdict(list)

        self.fights_counter = AsyncCounter()
        self.fights_on_maps = defaultdict(dict)

        self.game_actions_counter = AsyncCounter()
        self.game_actions = defaultdict(dict)

    async def broadcast_on_map(self, packet, map_id):
        await asyncio.gather(
            *[self.characters_server[character.id].write(packet) for character in self.characters_on_maps[map_id]]
        )

    async def broadcast_to_fight(self, packet, fight):
        await asyncio.gather(*[server.write(packet) for server in fight.servers if server])

    def character_connected(self, character, game_server):
        self.characters_server[character.id] = game_server

    def character_disconnected(self, character):
        del self.characters_server[character.id]

    def character_joined_map(self, character, map_):
        self.characters_on_maps[map_.id].append(character)

    def character_left_map(self, character, map_):
        self.characters_on_maps[map_.id].remove(character)

    async def broadcast_map_update(self, map_):
        await asyncio.gather(
            *[
                self.broadcast_on_map(
                    character.format_gm(),
                    map_.id,
                )
                for character in self.characters_on_maps[map_.id]
            ]
        )

    async def broadcast_move_action(self, game_action_id, character_id, map_id, path):
        await self.broadcast_on_map(
            ";".join([f"GA{game_action_id}", "1", str(character_id), f"a{path}"]),
            map_id,
        )

    async def broadcast_character_left_map(self, character_id, map_id):
        await self.broadcast_on_map(f"GM|-{character_id}", map_id)

    def pop_action(self, action_id):
        return self.game_actions.pop(action_id)

    async def ga_move(self, character, destination):
        action_id = await self.game_actions_counter()
        self.game_actions[action_id] = {
            "kind": GameActions.MOVE,
            "character": character,
            "destination": destination,
        }
        return action_id

    async def fight_started(self, fight):
        fight.state = fight.States.PLACEMENT
        fight.id = await self.fights_counter()
        self.fights_on_maps[fight.map_id][fight.id] = fight

    async def broadcast_fight_count(self, map_id):
        count = len(self.fights_on_maps[map_id].keys())
        if not count:
            return
        await self.broadcast_on_map(f"fC{count}", map_id)

    async def broadcast_new_map_fight_flag(self, map_id, fight):
        await self.broadcast_on_map(await fight.format_gc(), map_id)

    async def broadcast_all_fighters_joined_fight(self, fight):
        await asyncio.gather(
            *[
                self.broadcast_to_fight(fighter.format_gt(), fight)
                for _, team in fight.teams.items()
                for fighter in team
            ]
        )

        await self.broadcast_to_fight(
            "GM"
            + "".join(
                [f"|+{fighter.format_gm()}" for _, team in fight.teams.items() for fighter in team],
            ),
            fight,
        )

    async def broadcast_ga_to_fight(self, packet, fight):
        await self.broadcast_to_fight(packet, fight)
