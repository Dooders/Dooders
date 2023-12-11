import pygame
from pygame.locals import *
from dooders.sdk.base.coordinate import Coordinate
from dooders.game.constants import *
from dooders.game.entity import Entity
from dooders.game.modes import ModeController
from dooders.game.sprites import GhostSprites

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.pacman import PacMan


class Blinky(Entity):
    """
    Blinky class
    """

    def __init__(self) -> None:
        Entity.__init__(self)
        self.name = BLINKY
        self.color = RED
        self.alive = True
        self.sprites = GhostSprites(self)
        self.home = Coordinate(13, 14)
        self.position = self.home
        self.mode = ModeController(self)
        self.path = []
        self.waypoints = [113, 314, 113]

    def reset(self) -> None:
        """
        Calls the reset method of the parent class (Entity) to reset its attributes.

        Resets specific attributes of the Ghost class, including points
        and directionMethod.
        """
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goal_direction

    def update(self, game) -> None:
        """
        Calls the update method of the parent class (Entity) to update the
        ghost's position.

        Calls the update method of the mode object to handle the ghost's behavior
        based on its current mode (scatter, chase, etc.).

        Depending on the current mode, it either calls the scatter method or
        the chase method.

        The Entity.update method is then called to update the ghost's position
        based on its behavior.

        Parameters
        ----------
        dt : int
            The time increment.
        """
        dt = game.dt
        self.sprites.update(dt)
        self.next_move(game)
        # self.mode.update(dt)
        # if self.mode.current is SCATTER:
        #     self.scatter()
        # elif self.mode.current is CHASE:
        #     self.chase()
        Entity.update(self, game)

    def get_path(self, game) -> None:
        if self.path == [] and self.waypoints != []:
            next_waypoint = self.waypoints.pop(0)
            self.path = game.graph.path_finding(self.position, next_waypoint)

    def next_move(self, game) -> None:
        self.get_path(game)
        if self.path != []:
            next_position = self.path.pop(0)
            self.position = next_position
            self.direction = self.position.relative_direction(next_position)

    def scatter(self) -> None:
        """
        Sets the goal attribute to Coordinate()
        """
        self.goal = Coordinate()

    def chase(self) -> None:
        """
        Sets the goal attribute to the position of the pacman entity,
        indicating that the ghost is chasing the player.
        """
        self.goal = self.pacman.position

    def spawn(self) -> None:
        """
        Sets the goal attribute to the position of a spawn node
        """
        self.goal = self.spawnNode.position

    def set_spawn_node(self, space: "Space") -> None:
        """
        Sets the spawnNode attribute to a specific node where the ghost
        should spawn.

        Parameters
        ----------
        node : Node
            The node that the ghost should spawn at.
        """
        self.spawnNode = space

    def start_spawn(self) -> None:
        """
        Sets the ghost's mode to spawn mode using the mode.set_spawn_mode() method.

        If the current mode is spawn mode, it sets the ghost's speed,
        direction method, and goal to appropriate values for spawning.
        """
        self.mode.set_spawn_mode()
        if self.mode.current == SPAWN:
            self.set_speed(150)
            self.directionMethod = self.goal_direction
            self.spawn()

    def start_freight(self) -> None:
        """
        Sets the ghost's mode to freight mode using the mode.set_freight_mode() method.

        If the current mode is freight mode, it sets the ghost's speed and direction
        method for freight mode behavior.
        """
        self.mode.set_freight_mode()
        if self.mode.current == FREIGHT:
            self.set_speed(50)
            self.directionMethod = self.random_direction

    def normal_mode(self) -> None:
        """
        Resets the ghost to normal mode, setting its speed and direction method
        accordingly.

        It also denies access to a particular direction at the home node.
        """
        self.set_speed(100)
        self.directionMethod = self.goal_direction
        self.homeNode.deny_access(DOWN, self)
