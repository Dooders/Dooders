import numpy as np
import pygame

from dooders.game.constants import *
from dooders.sdk.base.coordinate import Coordinate
from dooders.game.npc import NPC


class Pellet(NPC):
    """
    This class provides a structured way to represent and manage a pellet in a game.

    It allows for easy rendering of the pellet, checking its visibility,
    and accessing its point value.

    Attributes
    ----------
    name : str
        Name of the pellet
    position : Coordinate
        Position of the pellet
    color : tuple
        Color of the pellet
    radius : int
        Radius of the pellet
    collideRadius : int
        Collision radius of the pellet
    points : int
        Point value of the pellet
    visible : bool
        Whether the pellet is visible or not

    Methods
    -------
    render(screen)
        Renders the pellet on the provided screen (or surface) if it's visible.
    """

    def __init__(self, row: int, column: int) -> None:
        """
        Initializes the pellet's name (PELLET).

        Sets the pellet's position based on the provided row and column,
        adjusted for the tile width and height.

        Defines the pellet's color (WHITE).

        Sets the pellet's radius and collision radius (both are set to a
        fraction of the tile width).

        Initializes the pellet's point value (points attribute) to 10.

        Initializes the pellet's visibility state (visible attribute) to True.

        Parameters
        ----------
        row : int
            Row index of the pellet
        column : int
            Column index of the pellet
        """
        NPC.__init__(self)
        self.name = PELLET
        self.position = Coordinate(column, row)
        self.color = WHITE
        self.radius = int(2 * TILEWIDTH / 16)
        self.collideRadius = 2 * TILEWIDTH / 16
        self.points = 10
        self.visible = True

    def render(self, screen: pygame.Surface) -> None:
        """
        Renders the pellet on the provided screen (or surface) if it's visible.

        Adjusts the pellet's position to the center of the tile and then draws
        a circle representing the pellet.

        Parameters
        ----------
        screen : pygame.Surface
            Screen or surface on which the pellet is drawn
        """
        if self.visible:
            x, y = self.position.as_pixel()
            position = (x + TILEWIDTH / 2, y + TILEHEIGHT / 2)
            pygame.draw.circle(screen, self.color, position, self.radius)


class PowerPellet(Pellet):
    """
    This class provides a structured way to represent and manage a power pellet
    in a game.

    It inherits the basic properties and behaviors of a regular pellet from the
    Pellet class and adds unique attributes and behaviors specific to power pellets,
    such as a larger size, higher point value, and a flashing effect.

    Attributes
    ----------
    name : str
        Name of the pellet
    position : Coordinate
        Position of the pellet
    color : tuple
        Color of the pellet
    radius : int
        Radius of the pellet
    collideRadius : int
        Collision radius of the pellet
    points : int
        Point value of the pellet
    visible : bool
        Whether the pellet is visible or not
    flashTime : float
        Duration for which the pellet should flash (toggle visibility)
    timer : float
        Elapsed time since the pellet started flashing

    Methods
    -------
    update(dt)
        Increments the timer by the time delta (dt). If the timer exceeds or
        equals the flash duration, it toggles the pellet's visibility and
        resets the timer. This creates a flashing effect for the power pellet,
        making it distinct from regular pellets.
    """

    def __init__(self, row: int, column: int) -> None:
        """
        Calls the initialization method of the parent Pellet class to set up basic attributes.

        Changes the pellet's name to POWERPELLET.

        Adjusts the pellet's radius to be larger than a regular pellet.

        Sets the pellet's point value (points attribute) to 50, which is higher than a regular pellet.

        Initializes the flashTime attribute, which determines how frequently the power pellet will flash (toggle visibility).

        Initializes a timer (timer attribute) to track the flashing effect.

        Parameters
        ----------
        row : int
            Row index of the pellet
        column : int
            Column index of the pellet
        """
        Pellet.__init__(self, row, column)
        self.name = POWERPELLET
        self.radius = int(8 * TILEWIDTH / 16)
        self.points = 50
        self.flashTime = 0.2
        self.timer = 0

    def update(self, dt: float) -> None:
        """
        Increments the timer by the time delta (dt).

        If the timer exceeds or equals the flashTime, it toggles the pellet's
        visibility and resets the timer. This creates a flashing effect for the
        power pellet, making it distinct from regular pellets.

        Parameters
        ----------
        dt : float
            Time delta
        """
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0


class PelletGroup:
    """
    This class provides a structured way to represent and manage all pellets in
    a game.

    It allows for easy creation of pellets based on a file, updating the state
    of power pellets, checking if all pellets have been eaten, and rendering all
    pellets on the screen.

    Attributes
    ----------
    pellet_List : list
        List of all pellets in the game
    powerpellets : list
        List of all power pellets in the game
    numEaten : int
        Number of pellets eaten by the player

    Methods
    -------
    update(dt)
        Updates all power pellets in the powerpellets list. This is mainly to
        handle the flashing effect of power pellets.
    create_pellet_list(pellet_file)
        Reads the pellet file and creates Pellet or PowerPellet objects based
        on the file's content.
    read_pellet_file(text_file)
        Reads the pellet layout from a file and returns it as a NumPy array.
    is_empty()
        Checks if the pellet_List is empty, i.e., all pellets have been eaten.
    render(screen)
        Renders all pellets in the pellet_List on the provided screen (or surface).
    """

    def __init__(self, pellet_file: str) -> None:
        """
        Initializes the pellet_List to store all pellets (both regular and
        power pellets).

        Initializes the powerpellets list to store only power pellets.

        Calls the create_pellet_list method to populate the pellet_List based on the
        provided pellet file.

        Initializes a counter (numEaten) to track the number of pellets eaten.

        Parameters
        ----------
        pellet_file : str
            Path to the pellet file
        """
        self.pellet_List = []
        self.powerpellets = []
        self.create_pellet_list(pellet_file)
        self.numEaten = 0

    def update(self, dt: float) -> None:
        """
        Updates all power pellets in the powerpellets list.

        This is mainly to handle the flashing effect of power pellets.

        Parameters
        ----------
        dt : float
            Time delta
        """
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)

    def create_pellet_list(self, pellet_file: str) -> None:
        """
        Reads the pellet file and creates Pellet or PowerPellet objects based
        on the file's content.

        Regular pellets are represented by '.' or '+', while power pellets are
        represented by 'P' or 'p'.

        Parameters
        ----------
        pellet_file : str
            Path to the pellet file
        """
        data = self.read_pellet_file(pellet_file)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in [".", "+"]:
                    self.pellet_List.append(Pellet(row, col))
                elif data[row][col] in ["P", "p"]:
                    pp = PowerPellet(row, col)
                    self.pellet_List.append(pp)
                    self.powerpellets.append(pp)

    def read_pellet_file(self, text_file: str) -> np.ndarray:
        """
        Reads the pellet layout from a file and returns it as a NumPy array.

        Parameters
        ----------
        text_file : str
            Path to the pellet file

        Returns
        -------
        np.ndarray
            Pellet layout as a NumPy array
        """
        return np.loadtxt(text_file, dtype="<U1")

    def is_empty(self) -> bool:
        """
        Checks if the pellet_List is empty, i.e., all pellets have been eaten.

        Returns
        -------
        bool
            Whether the pellet_List is empty or not
        """
        if len(self.pellet_List) == 0:
            return True
        return False

    def check_empty(self, x, y) -> bool:
        """
        Checks if the pellet_List is empty, i.e., all pellets have been eaten.
        """

        for pellet in self.pellet_List:
            if pellet.position.x == x and pellet.position.y == y:
                return False

        return True

    def render(self, screen: pygame.Surface) -> None:
        """
        Renders all pellets in the pellet_List on the provided screen (or surface).

        Parameters
        ----------
        screen : pygame.Surface
            Screen or surface on which the pellets are drawn
        """
        for pellet in self.pellet_List:
            pellet.render(screen)
