from typing import TYPE_CHECKING

import pygame
from pygame.locals import *

from dooders.game.constants import *
from dooders.game.entity import Entity
from dooders.game.modes import ModeController
from dooders.game.sprites import GhostSprites
from dooders.sdk.base.coordinate import Coordinate

if TYPE_CHECKING:
    from game.pacman import PacMan


class Ghost(Entity):
    """
    Class is responsible for managing the behavior and attributes of ghost
    characters in a game.

    It handles their movement, goals, modes (such as scatter and chase),
    and other properties related to gameplay.

    Attributes
    ----------
    name : str
        The name of the ghost.
    points : int
        The points value of the ghost.
    goal : Coordinate
        The goal of the ghost.
    directionMethod : method
        The method used to determine the direction of the ghost.
    pacman : Pacman
        The player character.
    mode : ModeController
        The mode controller for the ghost.
    blinky : Ghost
        Another ghost.
    homeNode : Node
        The node that the ghost should return to when it is in scatter mode.
    spawnNode : Node
        The node that the ghost should spawn at.
    sprites : GhostSprites
        The sprites associated with the ghost.

    Methods
    -------
    reset()
        Resets the ghost to its initial state.
    update(dt)
        Updates the ghost.
        Calls the update method of the sprites attribute.
        Calls the update method of the mode attribute.
        If the current mode is scatter, it calls the scatter method.
        If the current mode is chase, it calls the chase method.
        Calls the update method of the parent class (Entity).
    scatter()
        Sets the goal attribute to Vector2().
    chase()
        Sets the goal attribute to the position of the player character.
    spawn()
        Sets the goal attribute to the position of the spawn node.
    set_spawn_node(node)
        Sets the spawnNode attribute to the provided node.
    start_spawn()
        Sets the mode to spawn mode.
        If the current mode is spawn, it sets the speed to 150, sets the
        directionMethod to goal_direction, and calls the spawn method.
    start_freight()
        Sets the mode to freight mode.
        If the current mode is freight, it sets the speed to 50 and sets the
        directionMethod to random_direction.
    normal_mode()
        Sets the speed to 100 and sets the directionMethod to goal_direction.
    """

    def __init__(self, node, pacman=None, blinky=None) -> None:
        """
        Parameters
        ----------
        node : Node
            The node that the ghost should be positioned at.
        pacman : Pacman
            The player character.
        blinky : Ghost
            Another ghost. Used for the Inky ghost.
        """
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Coordinate()
        self.directionMethod = self.goal_direction
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homeNode = node
        self.home = Coordinate()

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
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, game)

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


class Blinky(Ghost):
    """Blinky is the red ghost."""

    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = BLINKY
        self.color = RED
        self.sprites = GhostSprites(self)


class Pinky(Ghost):
    """Pinky is the pink ghost."""

    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = PINKY
        self.color = PINK
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Coordinate(TILEWIDTH * NCOLS, 0)

    def chase(self):
        self.goal = (
            self.pacman.position
            + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4
        )


class Inky(Ghost):
    """Inky is the blue ghost."""

    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = INKY
        self.color = TEAL
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Coordinate(TILEWIDTH * NCOLS, TILEHEIGHT * NROWS)

    def chase(self):
        vec1 = (
            self.pacman.position
            + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
        )
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2


class Clyde(Ghost):
    """Clyde is the orange ghost."""

    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = CLYDE
        self.color = ORANGE
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Coordinate(0, TILEHEIGHT * NROWS)

    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitude_squared()
        if ds <= (TILEWIDTH * 8) ** 2:
            self.scatter()
        else:
            self.goal = (
                self.pacman.position
                + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4
            )


class GhostGroup:
    """
    Class is used to manage a group of ghost entities in a game or simulation.

    It provides methods for updating their behavior, changing their states,
    rendering them, and performing other group-level actions.

    Attributes
    ----------
    blinky : Blinky
        The red ghost.
    pinky : Pinky
        The pink ghost.
    inky : Inky
        The blue ghost.
    clyde : Clyde
        The orange ghost.
    ghosts : list
        A list of ghost entities.

    Methods
    -------
    __iter__()
        Returns an iterator for the ghosts attribute.
    update(dt)
        Calls the update method for each ghost entity in the group, effectively
        updating their positions and behavior based on elapsed time (dt).
    start_freight()
        Initiates freight mode for all the ghost entities in the group by
        calling the start_freight method on each ghost.
    set_spawn_node(node)
        Sets the spawn node for all ghost entities in the group by calling
        the set_spawn_node method on each ghost.
    update_points()
        Updates the points attribute for all ghost entities by doubling
        their current points.
    reset_points()
        Resets the points attribute for all ghost entities to 200.
    hide()
        Sets the visible attribute to False for all ghost entities,
        effectively hiding them.
    show()
        Sets the visible attribute to True for all ghost entities,
        effectively showing them.
    reset()
        Calls the reset method on each ghost entity to reset their
        attributes and state.
    render(screen)
        Calls the render method on each ghost entity to render them on
        the game screen.
    """

    def __init__(self, node: "Node", pacman: "PacMan") -> None:
        """
        Parameters
        ----------
        node : Node
            The node that the ghosts should be positioned at.
        pacman : Pacman
            The player character.
        """
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self) -> iter:
        """
        Returns
        -------
        iter
            An iterator for the ghosts attribute.
        """
        return iter(self.ghosts)

    def update(self, game) -> None:
        """
        Calls the update method for each ghost entity in the group, effectively
        updating their positions and behavior based on elapsed time (dt).

        Parameters
        ----------
        dt : int
            The time increment.
        """
        for ghost in self:
            ghost.update(game)

    def start_freight(self) -> None:
        """
        Initiates freight mode for all the ghost entities in the group by
        calling the start_freight method on each ghost.
        """
        for ghost in self:
            ghost.start_freight()
        self.reset_points()

    def set_spawn_node(self, node: "Node") -> None:
        """
        Sets the spawn node for all ghost entities in the group by calling
        the set_spawn_node method on each ghost.

        Parameters
        ----------
        node : Node
            The node that the ghosts should spawn at.
        """
        for ghost in self:
            ghost.set_spawn_node(node)

    def update_points(self) -> None:
        """
        Updates the points attribute for all ghost entities by doubling
        their current points.
        """
        for ghost in self:
            ghost.points *= 2

    def reset_points(self) -> None:
        """
        Resets the points attribute for all ghost entities to 200.
        """
        for ghost in self:
            ghost.points = 200

    def hide(self) -> None:
        """
        Sets the visible attribute to False for all ghost entities,
        effectively hiding them.
        """
        for ghost in self:
            ghost.visible = False

    def show(self) -> None:
        """
        Sets the visible attribute to True for all ghost entities,
        effectively showing them.
        """
        for ghost in self:
            ghost.visible = True

    def reset(self) -> None:
        """
        Calls the reset method on each ghost entity to reset their
        attributes and state.
        """
        for ghost in self:
            ghost.reset()

    def render(self, screen: "pygame.Surface") -> None:
        """
        Calls the render method on each ghost entity to render them on
        the game screen.

        Parameters
        ----------
        screen : pygame.Surface
            The game screen.
        """
        for ghost in self:
            ghost.render(screen)
