from typing import TYPE_CHECKING, List

from dooders.games.pacman.settings import Colors, GhostStates, SpawnPositions
from dooders.games.npc import NPC
from dooders.games.pacman.sprites import GhostSprites
from dooders.games.pacman.states import GhostState
from dooders.games.pacman.targets import GhostTarget
from dooders.sdk.base.coordinate import Coordinate

if TYPE_CHECKING:
    from dooders.games.pacman.game import Game


class Ghost(NPC):
    """
    Blinky is the red ghost. He is the most aggressive of the ghosts and will
    always try to chase PacMan.

    Attributes
    ----------
    color : tuple
        The color of the entity
    alive : bool
        Whether the entity is alive or not
    direction : Coordinate
        The direction the entity is moving in
    sprites : GhostSprites
        The sprites for the entity
    spawn : Coordinate
        The spawn position of the entity
    position : Coordinate
        The current position of the entity
    state : GhostState
        The state of the entity
    previous_position : Coordinate
        The previous position of the entity
    path : List[Coordinate]
        The path the entity to reach its target
    target : GhostTarget
        The target the entity is currently following

    Methods
    -------
    update(game: Game)
        Updates the entity
    start_freight()
        Starts the entity's freight state
    start_spawn()
        Sets the entity's state to spawn mode
    """

    def __init__(self) -> None:
        super().__init__()
        self.color = Colors.RED.value
        self.alive = True
        self.points = 200
        self.sprites = GhostSprites(self)
        self.spawn = Coordinate(SpawnPositions.BLINKY)
        self.position = self.spawn
        self.previous_position = self.position
        self.state = GhostState(self)
        self.path: List[Coordinate] = []
        self.target = GhostTarget()
        self.waypoints = [
            (6, 17),
            (6, 4),
            (1, 4),
            (1, 8),
            (6, 8),
            (6, 4),
            (1, 4),
            (1, 8),
            (1, 8),
        ]

    def update(self, game: "Game") -> None:
        """
        Updates the ghost's position and direction based on the current state.

        Parameters
        ----------
        game : Game
            The game controller object that the ghost is in.
        """
        time_delta = game.dt
        current_position = self.position.copy()
        self.sprites.update(time_delta)
        self.state.update(time_delta)
        self.target.update(game, self)
        self.next_move(game)
        self.previous_position = current_position

    def next_move(self, game: "Game") -> None:
        """
        Determines the next move for the ghost based on the current state.

        Parameters
        ----------
        game : Game
            The game controller object that the ghost is in.
        """
        self.find_path(game)

        if self.state.current == GhostStates.FREIGHT:
            if len(self.path) == 1:
                self.target.current = game.pacman.position

        self.move()

    def start_freight(self) -> None:
        """
        Starts the ghost's freight state.
        """
        self.state.freight()
        self.target.current = self.spawn

    def start_spawn(self) -> None:
        """
        Sets the ghost's state to spawn mode.
        """
        self.state.spawn()
        self.target.current = self.spawn


class Blinky(Ghost):
    def __init__(self):
        super().__init__()
