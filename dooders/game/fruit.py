import pygame

from dooders.game.settings import *
from dooders.game.sprites import FruitSprites
from dooders.sdk.base.coordinate import Coordinate


class Fruit:
    """
    Represents a fruit object within the game or simulation.

    It keeps track of attributes such as its position, color, points value,
    and a timer to determine its lifespan.

    When the timer exceeds the specified lifespan, the fruit is marked for destruction.

    Attributes
    ----------
    name : str
        The name of the fruit.
    color : tuple
        The color of the fruit.
    lifespan : int
        The lifespan of the fruit in seconds.
    timer : int
        The elapsed time since the fruit was created.
    destroy : bool
        Indicates whether the fruit should be destroyed.
    points : int
        The points value of the fruit.
    sprites : FruitSprites
        The sprites associated with the fruit.

    Methods
    -------
    update(dt)
        Updates the timer attribute by adding the elapsed time (dt).

        Checks if the timer has exceeded the lifespan, indicating that the fruit
        should be destroyed. If so, it sets the destroy attribute to True.
    """

    def __init__(self, level: int = 0) -> None:
        """
        Calls the __init__ method of the parent class (Entity) to initialize
        its attributes.

        Sets the name attribute to "FRUIT."

        Sets the color attribute to represent the color of the fruit.

        Initializes lifespan to 5 and timer to 0. These attributes seem to be
        used for determining how long the fruit should stay on the screen.

        Initializes destroy as False, indicating that the fruit is not marked
        for destruction.

        Calculates the points attribute based on the provided level.

        Calls the set_between_nodes method with the RIGHT direction, presumably
        positioning the fruit accordingly.

        Creates a FruitSprites object and assigns it to the sprites attribute.

        Parameters
        ----------
        node : Node
            The node that the fruit should be positioned at.
        level : int
            The current level of the game.
        """
        self.name = FRUIT
        self.color = Colors.GREEN
        self.lifespan = 5
        self.timer = 0
        self.destroy = False
        self.points = 100 + level * 20
        # self.set_between_nodes(RIGHT)
        self.sprites = FruitSprites(self, level)
        self.position = Coordinate(8, 2)

    def update(self, game) -> None:
        """
        Updates the timer attribute by adding the elapsed time (dt).

        Checks if the timer has exceeded the lifespan, indicating that the fruit
        should be destroyed. If so, it sets the destroy attribute to True.

        Parameters
        ----------
        dt : int
            The elapsed time since the last update.
        """
        dt = game.dt
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True
