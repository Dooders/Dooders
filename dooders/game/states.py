from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

from dooders.sdk.base.coordinate import Coordinate

if TYPE_CHECKING:
    from dooders.game.ghosts import Ghost


class GhostState(ABC):
    @abstractmethod
    def handle_behavior(self, ghost: Ghost):
        raise NotImplementedError


class ChaseState(GhostState):
    def handle_behavior(self, ghost: Ghost):
        pass


class ScatterState(GhostState):
    def handle_behavior(self, ghost: Ghost, game):
        # Set the target to the ghost's scatter corner
        # ghost.target = ghost.scatter_corner
        ghost.target = Coordinate(1, 4)  #! temp hard coded
        ghost.get_path(game)
        ghost.move()


class FrightenedState(GhostState):
    def handle_behavior(self, ghost: Ghost):
        pass


class EatenState(GhostState):
    def handle_behavior(self, ghost: Ghost, game):
        ghost.target = ghost.spawn
        ghost.get_path(game)
        ghost.move()


class GhostExample:
    def __init__(self, name: str):
        self.name = name
        self.state = ScatterState()  # Default state

    def set_state(self, state):
        self.state = state

    def behave(self):
        self.state.handle_behavior(self)


inky = Ghost("Inky")
inky.behave()  # Inky scatters

inky.set_state(ChaseState())
inky.behave()  # Inky chases

inky.set_state(FrightenedState())
inky.behave()  # Inky is frightened

inky.set_state(EatenState())
inky.behave()  # Inky is eaten and returns to the ghost house
