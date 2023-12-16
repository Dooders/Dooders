from typing import Union

from pygame.locals import *

from dooders.game.constants import (
    PACMAN,
    TILEHEIGHT,
    TILEWIDTH,
    Colors,
    Directions,
)
from dooders.game.models import FSM
from dooders.game.npc import NPC
from dooders.game.pellets import Pellet
from dooders.game.sprites import PacManSprites
from dooders.sdk.base.coordinate import Coordinate


class PacMan(NPC):
    """
    PacMan class

    PacMan is the main character of the game. He is controlled by the player
    and must eat all the pellets in the maze while avoiding the ghosts.

    Attributes
    ----------
    name : string
        The name of the entity
    color : tuple
        The color of the entity
    direction : int
        The direction the entity is moving
    alive : bool
        Whether or not the entity is alive
    sprites : PacManSprites
        The sprites for the entity

    Methods
    -------
    reset()
        Resets the entity
    die()
        Kills the entity
    update(dt)
        Updates the entity
    get_valid_key()
        Gets the key pressed by the player
    eat_pellets(pellet_List)
        Checks if the entity has eaten a pellet
    collide_ghost(ghost)
        Checks if the entity has collided with a ghost
    collide_check(other)
        Checks if the entity has collided with another entity
    """

    def __init__(self) -> None:
        NPC.__init__(self)
        self.name = PACMAN
        self.color = Colors.YELLOW.value
        self.alive = True
        self.direction = Directions.STOP
        self.sprites = PacManSprites(self)
        self.home = Coordinate(13, 26)
        self.position = self.home
        self.state = FSM()
        self.previous_position = self.position
        self.path = []
        self.target = None

    def find_path(self, game) -> None:
        self.path = game.graph.path_finding(self.position, self.target)

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

    def reset(self) -> None:
        """
        Resets the Pac-Man to its initial state, facing left and alive.
        It also resets its sprites.
        """
        self.position = self.home
        self.alive = True
        self.image = self.sprites.get_start_image()
        self.sprites.reset()

    def die(self) -> None:
        """
        Sets the Pac-Man's state to dead and stops its movement.
        """
        self.alive = False

    def update(self, game) -> None:
        """
        Updates the Pac-Man's state based on the time delta (dt).

        It handles the movement, checks for overshooting targets, and handles
        portal transitions (like when Pac-Man goes off one side of the screen
        and appears on the other). It also checks for direction reversal.

        Parameters
        ----------
        dt : float
            The time delta
        """
        dt = game.dt
        self.sprites.update(dt)

        if self.alive:
            current_position = self.position.copy()
            self.target = self.state.update(game, self)
            self.find_path(game)
            self.move()
            self.previous_position = current_position

    def eat_pellets(self, pellet_List: list) -> Union[None, object]:
        """
        Checks for collisions between Pac-Man and any pellet in the provided list.

        If a collision is detected, it returns the pellet that was "eaten".

        Parameters
        ----------
        pellet_List : list
            A list of pellets to check for collisions with

        Returns
        -------
        object
            The pellet that was "eaten" if a collision is detected, None otherwise
        """
        for pellet in pellet_List:
            if self.collide_check(pellet):
                return pellet
        return None

    def collide_ghost(self, ghost: "Ghost") -> bool:
        """
        Checks if Pac-Man has collided with a ghost.

        Returns True if a collision is detected, False otherwise.

        Parameters
        ----------
        ghost : Ghost
            The ghost to check for collisions with

        Returns
        -------
        bool
            True if a collision is detected, False otherwise
        """
        return self.collide_check(ghost)

    def collide_check(self, other: "object") -> bool:
        """

        Returns True if a collision is detected, False otherwise.

        Parameters
        ----------
        other : object
            The entity to check for collisions with

        Returns
        -------
        bool
            True if a collision is detected, False otherwise
        """
        if self.position == other.position:
            return True

    def render(self, screen):
        if self.visible:
            if self.image is not None:
                x, y = self.position.as_pixel()
                position = (x - TILEWIDTH / 2, y - TILEHEIGHT / 2)
                screen.blit(self.image, position)
            else:
                raise Exception("No image for PacMan")
