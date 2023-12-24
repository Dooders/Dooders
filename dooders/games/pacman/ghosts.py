from typing import TYPE_CHECKING, List

import pygame

from dooders.games.npc import NPC
from dooders.games.pacman.behavior import GhostBehavior
from dooders.games.pacman.settings import (
    Colors,
    Dimensions,
    GhostStates,
    SpawnPositions,
)
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
        self.behavior = GhostBehavior(self)
        self.waypoints = [
            (6, 17),
            (6, 4),
            (1, 4),
            (1, 8),
            (6, 8),
            (6, 4),
            (1, 4),
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
        self.behavior.model.run(game, self)
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

    # def render(self, screen: "pygame.Surface") -> None:
    #     """
    #     Renders the ghost on the game screen.

    #     Parameters
    #     ----------
    #     screen : pygame.Surface
    #         The game screen.
    #     """
    #     super().render(screen)
    #     # blit red dot for the target
    #     if self.target.current is not None:
    #         target = self.target.current
    #         if isinstance(target, tuple):
    #             target = Coordinate(target[0], target[1])

    #         x, y = target.as_pixel()
    #         position = (x - Dimensions.TILEWIDTH / 2, y - Dimensions.TILEHEIGHT / 2)
    #         pygame.draw.circle(screen, Colors.RED.value, position, 5)


class Pinky(Ghost):
    def __init__(self):
        super().__init__()
        self.color = Colors.PINK.value
        self.spawn = Coordinate(SpawnPositions.PINKY)
        self.waypoints = [(26, 4), (26, 29), (1, 29), (1, 4), (26, 4)]


class Inky(Ghost):
    def __init__(self):
        super().__init__()
        self.color = Colors.TEAL.value
        self.spawn = Coordinate(SpawnPositions.INKY)


class Clyde(Ghost):
    def __init__(self):
        super().__init__()
        self.color = Colors.ORANGE.value
        self.spawn = Coordinate(SpawnPositions.CLYDE)


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

    def __init__(self) -> None:
        """
        Parameters
        ----------
        node : Node
            The node that the ghosts should be positioned at.
        pacman : Pacman
            The player character.
        """
        self.blinky = Blinky()
        self.pinky = Pinky()
        self.inky = Inky()
        self.clyde = Clyde()
        self.ghosts: List[Ghost] = [self.blinky]

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

    @property
    def is_freight(self) -> bool:
        """
        Returns True if any of the ghosts are in freight mode, False otherwise.
        """
        for ghost in self:
            if ghost.state.current is GhostStates.FREIGHT:
                return True
        return False

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
