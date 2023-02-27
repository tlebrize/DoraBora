from dataclasses import field, dataclass
from dora_bora import game_actions
from .base_state import BaseState


@dataclass
class GameActionsState(BaseState):
    game_action_sequence: int = 0
    game_actions: dict = field(default_factory=dict)

    def _next_game_action_id(self):
        self.game_action_sequence += 1
        return self.game_action_sequence

    def move(self, character, target_cell):
        return self.add(game_actions.Move(character, target_cell))

    def pop(self, id_):
        return self.game_actions.pop(id_)

    def add(self, action):
        id_ = self._next_game_action_id()
        self.game_actions[id_] = action
        return id_
