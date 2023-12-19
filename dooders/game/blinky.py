from dooders.game.constants import (
    Colors,
    Dimensions,
    Directions,
    GhostStates,
    SpawnPositions,
)
from dooders.game.npc import NPC
from dooders.game.sprites import GhostSprites
from dooders.game.states import GhostState
from dooders.game.targets import GhostTarget
from dooders.sdk.base.coordinate import Coordinate


class Blinky(NPC):
    """
    Blinky class
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

    def get_path(self, game) -> None:
        self.path = game.graph.path_finding(self.position, self.target.current)

    def move(self) -> None:
        """
        Moves the ghost to the next position in its path.
        """
        if self.path != []:
            next_position = self.path.pop(0)
            if type(next_position) == tuple:
                next_position = Coordinate(next_position[0], next_position[1])
            self.direction = self.position.relative_direction(next_position)
            self.position = next_position

    def next_move(self, game) -> None:
        self.get_path(game)

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

    def reset(self) -> None:
        """
        Resets the ghost's position and direction to its spawn.
        """
        self.position = self.spawn
        self.direction = Directions.STOP
        self.visible = True

    def render(self, screen) -> None:
        """
        Renders the ghost's sprites on the screen.

        Parameters
        ----------
        screen : pygame.Surface
            The screen to render the sprites on.
        """
        if self.visible:
            if self.image is not None:
                x, y = self.position.as_pixel()
                position = (x - Dimensions.TILEWIDTH / 2, y - Dimensions.TILEHEIGHT / 2)
                screen.blit(self.image, position)
            else:
                raise Exception("No image for Blinky Ghost")
