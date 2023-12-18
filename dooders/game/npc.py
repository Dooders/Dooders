from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

import pygame

from dooders.game.constants import Dimensions, Directions
from dooders.sdk.base.coordinate import Coordinate
from dooders.sdk.utils.short_id import ShortUUID as short_id

if TYPE_CHECKING:
    from dooders.game.game import Game


class NPC(ABC):
    def __init__(self) -> None:
        self.seed = short_id()
        self.id = self.seed.uuid()
        self.name = self.__class__.__name__
        self.visible = True
        self.direction = Directions.STOP

    @abstractmethod
    def update(self) -> None:
        """
        Every NPC must implement this method.

        This method is called every cycle and is used to update the NPC's state.
        """
        raise NotImplementedError("update() method not implemented")

    def find_path(self, game: "Game") -> List[Coordinate]:
        """
        Finds the path from the NPC's current position to the target position.

        Parameters
        ----------
        game : Game
            The game object

        Returns
        -------
        List[Coordinate]
            The path from the NPC's current position to the target position,
            without the current position.
        """
        return game.graph.path_finding(self.position, self.target)

    def move(self) -> None:
        """
        Moves the NPC to the next position in its path.

        If the NPC has no path, it will not move.
        """
        if self.path != []:
            next_position = self.path.pop(0)
            if type(next_position) == tuple:
                next_position = Coordinate(next_position[0], next_position[1])
            self.direction = self.position.relative_direction(next_position)
            self.position = next_position

        else:
            self.direction = Directions.STOP

    def collide_check(self, other: "NPC") -> bool:
        """
        Checks if the NPC has collided with another NPC.

        Parameters
        ----------
        other : NPC
            The other NPC to check collision with.

        Returns
        -------
        bool
            Whether or not the two NPCs have collided.
        """
        return self.position == other.position

    def die(self) -> None:
        """
        Kills the NPC.
        """
        self.alive = False

    def reset(self) -> None:
        """
        Resets the NPC's position and direction to its spawn.
        """
        self.alive = True
        self.position = self.spawn
        self.direction = Directions.STOP
        self.visible = True
        self.image = self.sprites.get_start_image()

    def render(self, screen: "pygame.Surface") -> None:
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
                raise Exception(f"No image for {self.name} NPC")
