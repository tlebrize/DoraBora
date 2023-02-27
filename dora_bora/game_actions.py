from dataclasses import dataclass


@dataclass
class GameAction:
    ...


@dataclass
class Move(GameAction):
    character: int
    target_cell: int
