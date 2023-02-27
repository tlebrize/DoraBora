from .characters import CharactersState
from .maps import MapsState
from .game_actions import GameActionsState


class __SharedState:
    def __init__(self):
        self.characters = CharactersState(self)
        self.maps = MapsState(self)
        self.game_actions = GameActionsState(self)


__shared_state_singleton = __SharedState()


def get_shared_state():
    return __shared_state_singleton
