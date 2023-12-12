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
        Updates the ghost's position and direction based on the current mode.

        Parameters
        ----------
        game : GameController
            The game controller object that the ghost is in.
        """
        dt = game.dt

        self.sprites.update(dt)
        self.next_move(game)

    def get_path(self, game, target) -> None:
        self.path = game.graph.path_finding(self.position, target)

    def next_move(self, game) -> None:
        if self.path == [] and self.waypoints != []:
            target = self.waypoints.pop(0)
            self.get_path(game, target)

        if self.waypoints == []:
            target = game.pacman.position
            self.get_path(game, target)

        if self.path != []:
            next_position = self.path.pop(0)

            if type(next_position) == tuple:
                next_position = Coordinate(next_position[0], next_position[1])
            self.direction = self.position.relative_direction(next_position)
            self.position = next_position

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
                position = (x - TILEWIDTH / 2, y - TILEHEIGHT / 2)
                screen.blit(self.image, position)
            else:
                raise Exception("No image for Blinky Ghost")
