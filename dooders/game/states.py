from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dooders.game.game import Game
    from dooders.game.npc import NPC


class State(ABC):
    def __init__(self, npc: "NPC") -> None:
        self.timer = 0
        self.time = None
        self.current = None
        self.npc = npc

    @abstractmethod
    def update(self, game: "Game") -> None:
        """
        Must have an update method that takes in an NPC and a Game object and
        updates the NPC's state.
        """
        raise NotImplementedError("update() method not implemented")
