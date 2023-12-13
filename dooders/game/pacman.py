from typing import Union

from pygame.locals import *

from dooders.game.constants import *
from dooders.game.entity import Entity
from dooders.game.models import FSM
from dooders.game.pellets import Pellet
from dooders.game.sprites import PacManSprites
from dooders.sdk.base.coordinate import Coordinate


class PacMan(Entity):
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
        Entity.__init__(self)
        self.name = PACMAN
        self.color = YELLOW
        self.alive = True
        self.direction = LEFT
        self.sprites = PacManSprites(self)
        self.home = Coordinate(13, 26)
        self.position = self.home
        self.brain = FSM()

    def reset(self) -> None:
        """
        Resets the Pac-Man to its initial state, facing left and alive.
        It also resets its sprites.
        """
        Entity.reset(self)
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
            current_position = self.position
            next_position = self.logic(game)
            if next_position is not None:
                self.move(game, next_position)
                self.direction = current_position.relative_direction(next_position)

    def logic(self, game) -> None:
        next_position = self.brain.update(game, self)

        return next_position

    def move(self, game, coordinate: "Coordinate") -> None:
        self.position = coordinate

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
        return self.position == other.position
        # if isinstance(other, Pellet):
        #     return self.position == other.position
        # else:
        #     d = self.position - other.position
        #     dSquared = d.magnitude_squared()
        #     rSquared = (self.collideRadius + other.collideRadius) ** 2
        #     if dSquared <= rSquared:
        #         return True
        #     return False

    def render(self, screen):
        if self.visible:
            if self.image is not None:
                x, y = self.position.as_pixel()
                position = (x - TILEWIDTH / 2, y - TILEHEIGHT / 2)
                screen.blit(self.image, position)
            else:
                raise Exception("No image for PacMan")
