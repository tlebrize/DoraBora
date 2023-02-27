from dataclasses import field, dataclass
from collections import defaultdict
from .base_state import BaseState


@dataclass
class MapsState(BaseState):
    characters: defaultdict[dict] = field(
        default_factory=lambda: defaultdict(list),
    )
