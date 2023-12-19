from dooders.game.constants import Colors, GhostStates, SpawnPositions
from dooders.game.npc import NPC
from dooders.game.sprites import GhostSprites
from dooders.game.states import GhostState
from dooders.game.targets import GhostTarget
from dooders.sdk.base.coordinate import Coordinate


class Blinky(NPC):
    """
    Blinky is the red ghost. He is the most aggressive of the ghosts and will
    always try to chase PacMan.

    Attributes
    ----------
    color : tuple
        The color of the entity
    alive : bool
        Whether or not the entity is alive
    points : int
        The amount of points the entity is worth
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
    path : list
        The path the entity is following
    target : GhostTarget
        The target of the entity
    waypoints : list
        The waypoints the entity is following
    """

    def __init__(self) -> None:
        NPC.__init__(self)
        self.color = Colors.RED.value
        self.alive = True
        self.points = 200
        self.sprites = GhostSprites(self)
        self.spawn = Coordinate(SpawnPositions.BLINKY)
        self.position = self.spawn
        self.previous_position = self.position
        self.state = GhostState(self)
        self.path = []
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

    def update(self, game) -> None:
        """
        Updates the ghost's position and direction based on the current state.

        Parameters
        ----------
        game : GameController
            The game controller object that the ghost is in.
        """
        dt = game.dt
        current_position = self.position.copy()
        self.sprites.update(dt)
        self.state.update(dt)
        self.target.update(game, self)
        self.next_move(game)
        self.previous_position = current_position

    def next_move(self, game) -> None:
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

    def normal_mode(self) -> None:
        pass
