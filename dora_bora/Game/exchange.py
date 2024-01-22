import asyncio
from collections import defaultdict

from Game.server import GameServer
from Game.game_actions import GameActions


class Exchange:
    def __init__(self):
        self.client_lock = asyncio.Lock()
        self.client_counter = 0

        self.characters_server = {}
        self.characters_on_maps = defaultdict(list)

        self.game_actions_lock = asyncio.Lock()
        self.game_actions_counter = 0
        self.game_actions = defaultdict(dict)

    async def get_next_client_id(self):
        async with self.client_lock:
            self.client_counter += 1
            client_id = self.client_counter
        return client_id

    def character_connected(self, character, game_server):
        self.characters_server[character.id] = game_server

    def character_disconnected(self, character):
        del self.characters_server[character.id]

    def character_joined_map(self, character, map):
        self.characters_on_maps[map.id].append(character)

    def character_left_map(self, character, map):
        self.characters_on_maps[map.id].remove(character)

    async def broadcast_map_update(self, map):
        await asyncio.gather(
            *[
                self.characters_server[c.id].write(character.format_gm())
                for character in self.characters_on_maps[map.id]
                for c in self.characters_on_maps[map.id]
            ]
        )

    async def broadcast_move_action(self, game_action_id, character_id, map_id, path):
        await asyncio.gather(
            *[
                self.characters_server[c.id].write(
                    ";".join([f"GA{game_action_id}", "1", str(character_id), f"a{path}"])
                )
                for c in self.characters_on_maps[map_id]
            ]
        )

    async def broadcast_character_left_map(self, character_id, map_id):
        await asyncio.gather(
            *[self.characters_server[c.id].write(f"GM|-{character_id}") for c in self.characters_on_maps[map_id]]
        )

    async def ga_get_next_id(self):
        async with self.game_actions_lock:
            self.game_actions_counter += 1
            counter = self.game_actions_counter
        return counter

    def pop_action(self, action_id):
        return self.game_actions.pop(action_id)

    async def ga_move(self, character, destination):
        action_id = await self.ga_get_next_id()
        self.game_actions[action_id] = {
            "kind": GameActions.MOVE,
            "character": character,
            "destination": destination,
        }
        return action_id
