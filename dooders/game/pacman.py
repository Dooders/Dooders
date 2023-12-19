from typing import Union

from pygame.locals import *

from dooders.game.constants import Colors, Directions, SpawnPositions
from dooders.game.npc import NPC
from dooders.game.sprites import PacManSprites
from dooders.game.states import PacManState
from dooders.game.targets import PacManTarget
from dooders.sdk.base.coordinate import Coordinate


class PacMan(NPC):
    """
    PacMan is the main character of the game. He is controlled by the player
    and must eat all the pellets in the maze while avoiding the ghosts.

    Attributes
    ----------
    color : tuple
        The color of the entity
    direction : int
        The direction the entity is moving
    alive : bool
        Whether or not the entity is alive
    sprites : PacManSprites
        The sprites for the entity
    spawn : Coordinate
        The spawn position of the entity
    position : Coordinate
        The current position of the entity
    state : PacManState
        The state of the entity
    previous_position : Coordinate
        The previous position of the entity
    path : list
        The path the entity is following
    target : PacManTarget
        The target of the entity

    Methods
    -------
    update(dt)
        Updates the entity
    eat_pellets(pellet_List)
        Checks if the entity has eaten a pellet
    """

    def __init__(self) -> None:
        NPC.__init__(self)
        self.color = Colors.YELLOW.value
        self.alive = True
        self.direction = Directions.STOP
        self.sprites = PacManSprites(self)
        self.spawn = Coordinate(SpawnPositions.PACMAN)
        self.position = self.spawn
        self.state = PacManState(self)
        self.previous_position = self.position
        self.path = []
        self.target = PacManTarget()

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
            self.state.update(game)
            self.target.update(game, self)
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
