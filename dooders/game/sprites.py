import pygame
from dooders.game.constants import *
import numpy as np
from dooders.game.animation import Animator
from typing import TYPE_CHECKING

from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from pacman import PacMan
    from ghosts import Ghost
    from fruit import Fruit

BASETILEWIDTH = 16  # The width of a tile in the sprite sheet
BASETILEHEIGHT = 16  # The height of a tile in the sprite sheet
DEATH = 5  # Reference to the death animation in the sprite sheet


class Spritesheet(ABC):
    """
    Class is designed to handle sprite sheets in the game.

    A sprite sheet is a collection of multiple sprites (small images or
    animations) combined into a single image.

    Attributes
    ----------
    sheet : pygame.Surface
        The sprite sheet image.

    Methods
    -------
    get_image(x, y, width, height)
        Retrieves a specific sprite from the sprite sheet based on the given
        x, y, width, and height parameters.
    """

    def __init__(self) -> None:
        """
        Loads the sprite sheet image using the pygame library.

        Converts the image for better performance using the convert() method.

        Sets a transparent color key based on the color of the top-left pixel
        of the sprite sheet.

        Rescales the sprite sheet to match the game's tile width and height.
        """
        self.sheet = pygame.image.load("dooders/game/assets/spritesheet.png").convert()
        transcolor = self.sheet.get_at((0, 0))
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))

    def get_image(self, x: int, y: int, width: int, height: int) -> pygame.Surface:
        """
        Retrieves a specific sprite from the sprite sheet based on the given
        x, y, width, and height parameters.

        Parameters
        ----------
        x : int
            The x-coordinate of the sprite to retrieve from the sprite sheet.
        y : int
            The y-coordinate of the sprite to retrieve from the sprite sheet.
        width : int
            The width of the sprite to retrieve from the sprite sheet.
        height : int

        Returns
        -------
        pygame.Surface
            The sprite at the specified x and y coordinates.
        """
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())


class PacManSprites(Spritesheet):
    """
    This class provides a structured way to manage and update the visual
    representation of the Pac-Man character based on its state and direction.

    It encapsulates the logic for handling Pac-Man's animations and ensures
    that the correct sprite is displayed at the right time.

    Attributes
    ----------
    entity : Pacman
        The Pacman entity that the sprites are associated with.
    animations : dict
        A dictionary that maps directions to Animator objects.
    stopimage : tuple
        A tuple that stores the x and y coordinates of the image that should
        be displayed when Pacman is not moving.

    Methods
    -------
    define_animations()
        Defines the animations for each direction.
    update(dt)
        Updates the sprite based on the current direction of the entity.
    reset()
        Resets all of the animations.
    get_start_image()
        Returns the starting image for the entity.
    get_image(x, y)
        Returns the image at the specified x and y coordinates.
    """

    def __init__(self, entity: "PacMan") -> None:
        """
        Calls the initialization method of the parent Spritesheet class.

        Associates the PacmanSprites object with an entity (likely the Pac-Man
        character in the game).

        Sets the initial image of the entity to a starting image.

        Initializes an empty dictionary for animations.

        Defines the animations for Pac-Man using the define_animations method.

        Sets a default stopped image for Pac-Man.

        Parameters
        ----------
        entity : Pacman
            The Pacman entity that the sprites are associated with.
        """
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.get_start_image()
        self.animations = {}
        self.define_animations()
        self.stopimage = (8, 0)

    def define_animations(self) -> None:
        """
        Defines animations for Pac-Man based on its direction (LEFT, RIGHT, UP,
        DOWN) and a DEATH animation. Each animation is associated with a
        sequence of sprite positions on the sprite sheet.

        The Animator class (presumably defined elsewhere) seems to handle the
        sequence and timing of the animation frames.
        """
        self.animations[LEFT] = Animator(((8, 0), (0, 0), (0, 2), (0, 0)))
        self.animations[RIGHT] = Animator(((10, 0), (2, 0), (2, 2), (2, 0)))
        self.animations[UP] = Animator(((10, 2), (6, 0), (6, 2), (6, 0)))
        self.animations[DOWN] = Animator(((8, 2), (4, 0), (4, 2), (4, 0)))
        self.animations[DEATH] = Animator(
            (
                (0, 12),
                (2, 12),
                (4, 12),
                (6, 12),
                (8, 12),
                (10, 12),
                (12, 12),
                (14, 12),
                (16, 12),
                (18, 12),
                (20, 12),
            ),
            speed=6,
            loop=False,
        )

    def update(self, dt: float) -> None:
        """
        Updates the image of the associated entity based on its current state
        and direction.

        If Pac-Man is alive, it updates the image based on the direction it's moving.
        If Pac-Man is not moving (STOP direction), it uses the stopped image.
        If Pac-Man is not alive, it uses the DEATH animation.

        Parameters
        ----------
        dt : float
            The time elapsed since the last update.
        """
        if self.entity.alive == True:
            if self.entity.direction == LEFT:
                self.entity.image = self.get_image(*self.animations[LEFT].update(dt))
                self.stopimage = (8, 0)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.get_image(*self.animations[RIGHT].update(dt))
                self.stopimage = (10, 0)
            elif self.entity.direction == DOWN:
                self.entity.image = self.get_image(*self.animations[DOWN].update(dt))
                self.stopimage = (8, 2)
            elif self.entity.direction == UP:
                self.entity.image = self.get_image(*self.animations[UP].update(dt))
                self.stopimage = (10, 2)
            elif self.entity.direction == STOP:
                self.entity.image = self.get_image(*self.stopimage)
        else:
            self.entity.image = self.get_image(*self.animations[DEATH].update(dt))

    def reset(self) -> None:
        """
        Resets all the animations to their initial state.
        """
        for key in list(self.animations.keys()):
            self.animations[key].reset()

    def get_start_image(self) -> pygame.Surface:
        """
        Returns
        -------
        pygame.Surface
            The starting image for the entity.
        """
        return self.get_image(8, 0)

    def get_image(self, x: int, y: int) -> pygame.Surface:
        """
        Overrides the get_image method from the parent Spritesheet class to
        always retrieve a sprite of size 2 * TILEWIDTH by 2 * TILEHEIGHT.

        Parameters
        ----------
        x : int
            The x-coordinate of the sprite to retrieve from the sprite sheet.
        y : int
            The y-coordinate of the sprite to retrieve from the sprite sheet.

        Returns
        -------
        pygame.Surface
            The sprite at the specified x and y coordinates.
        """
        return Spritesheet.get_image(self, x, y, 2 * TILEWIDTH, 2 * TILEHEIGHT)


class GhostSprites(Spritesheet):
    """
    Class provides a structured way to manage and update the visual
    representation of the ghost characters based on their state, mode, and
    direction.

    It encapsulates the logic for handling the ghost's animations
    and ensures that the correct sprite is displayed at the right time.

    Parameters
    ----------
    entity : Ghost
        The ghost entity that the sprites are associated with.

    Attributes
    ----------
    entity : Ghost
        See above.
    x : dict
        A dictionary that maps each ghost name (BLINKY, PINKY, INKY, CLYDE) to
        its corresponding x-coordinate on the sprite sheet.

    Methods
    -------
    update(dt)
        Updates the sprite based on the current state, mode, and direction of
        the entity.
    get_start_image()
        Returns the starting image for the entity.
    get_image(x, y)
        Returns the image at the specified x and y coordinates.
    """

    def __init__(self, entity: "Ghost") -> None:
        """
        Calls the initialization method of the parent Spritesheet class.

        Sets up a dictionary self.x that maps each ghost name (BLINKY, PINKY,
        INKY, CLYDE) to its corresponding x-coordinate on the sprite sheet.

        Associates the GhostSprites object with an entity (likely a ghost
        character in the game).

        Sets the initial image of the entity to a starting image.

        Parameters
        ----------
        entity : Ghost
            The ghost entity that the sprites are associated with.
        """
        Spritesheet.__init__(self)
        self.x = {BLINKY: 0, PINKY: 2, INKY: 4, CLYDE: 6}
        self.entity = entity
        self.entity.image = self.get_start_image()

    def update(self, dt: float) -> None:
        """
        Updates the image of the associated ghost entity based on its current
        state, mode, and direction.

        If the ghost is in SCATTER or CHASE mode, its image is determined by its
            direction and its specific type (BLINKY, PINKY, etc.).
        If the ghost is in FREIGHT mode (when Pac-Man eats a power pellet and
            the ghosts become vulnerable), all ghosts use the same frightened image.
        If the ghost is in SPAWN mode (when it's respawning after being eaten),
            its image is determined by its direction but uses a common set of sprites.

        Parameters
        ----------
        dt : float
            The time elapsed since the last update.
        """
        x = self.x[self.entity.name]
        if self.entity.mode.current in [SCATTER, CHASE]:
            if self.entity.direction == LEFT:
                self.entity.image = self.get_image(x, 8)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.get_image(x, 10)
            elif self.entity.direction == DOWN:
                self.entity.image = self.get_image(x, 6)
            elif self.entity.direction == UP:
                self.entity.image = self.get_image(x, 4)
        elif self.entity.mode.current == FREIGHT:
            self.entity.image = self.get_image(10, 4)
        elif self.entity.mode.current == SPAWN:
            if self.entity.direction == LEFT:
                self.entity.image = self.get_image(8, 8)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.get_image(8, 10)
            elif self.entity.direction == DOWN:
                self.entity.image = self.get_image(8, 6)
            elif self.entity.direction == UP:
                self.entity.image = self.get_image(8, 4)

    def get_start_image(self) -> pygame.Surface:
        """
        Returns
        -------
        pygame.Surface
            The starting image for the entity.
        """
        return self.get_image(self.x[self.entity.name], 4)

    def get_image(self, x: int, y: int) -> pygame.Surface:
        """
        Overrides the get_image method from the parent Spritesheet class to
        always retrieve a sprite of size 2 * TILEWIDTH by 2 * TILEHEIGHT

        Parameters
        ----------
        x : int
            The x-coordinate of the sprite to retrieve from the sprite sheet.
        y : int
            The y-coordinate of the sprite to retrieve from the sprite sheet.

        Returns
        -------
        pygame.Surface
            The sprite at the specified x and y coordinates.
        """
        return Spritesheet.get_image(self, x, y, 2 * TILEWIDTH, 2 * TILEHEIGHT)


class FruitSprites(Spritesheet):
    """
    Handles the sprites for the fruit bonuses that appear in the Pac-Man game.

    Attributes
    ----------
    entity : Fruit
        The fruit entity that the sprites are associated with.
    fruits : dict
        A dictionary that maps each level (or index) to its corresponding x and
        y coordinates on the sprite sheet.

    Methods
    -------
    get_start_image(key)
        Returns the starting image for the fruit based on the provided key
        (which is determined by the level).
    get_image(x, y)
        Returns the image at the specified x and y coordinates.
    """

    def __init__(self, entity: "Fruit", level: int) -> None:
        """
        Calls the initialization method of the parent Spritesheet class.

        Associates the FruitSprites object with an entity (likely a fruit bonus
        in the game).

        Sets up a dictionary self.fruits that maps each level (or index) to
        its corresponding x and y coordinates on the sprite sheet. This dictionary
        defines the location of each fruit sprite on the sprite sheet.

        Sets the initial image of the entity to a starting image based on the
        current level. The level modulo the number of fruits (len(self.fruits))
        ensures that the fruit selection wraps around if the level number exceeds
        the number of available fruits.

        Parameters
        ----------
        entity : Fruit
            The fruit entity that the sprites are associated with.
        level : int
            The current level of the game.
        """
        Spritesheet.__init__(self)
        self.entity = entity
        self.fruits = {
            0: (16, 8),
            1: (18, 8),
            2: (20, 8),
            3: (16, 10),
            4: (18, 10),
            5: (20, 10),
        }
        self.entity.image = self.get_start_image(level % len(self.fruits))

    def get_start_image(self, key: int) -> pygame.Surface:
        """
        Returns the starting image for the fruit based on the provided key
        (which is determined by the level).

        Parameters
        ----------
        key : int
            The key to retrieve the fruit sprite from the self.fruits dictionary.

        Returns
        -------
        pygame.Surface
            The fruit sprite at the specified key.
        """
        return self.get_image(*self.fruits[key])

    def get_image(self, x: int, y: int) -> pygame.Surface:
        """
        Overrides the get_image method from the parent Spritesheet class to
        always retrieve a sprite of size 2 * TILEWIDTH by 2 * TILEHEIGHT.

        Parameters
        ----------
        x : int
            The x-coordinate of the sprite to retrieve from the sprite sheet.
        y : int
            The y-coordinate of the sprite to retrieve from the sprite sheet.

        Returns
        -------
        pygame.Surface
            The sprite at the specified x and y coordinates.
        """
        return Spritesheet.get_image(self, x, y, 2 * TILEWIDTH, 2 * TILEHEIGHT)


class LifeSprites(Spritesheet):
    """
    handle the sprites representing the number of lives the player has
    left in the Pac-Man game.

    Attributes
    ----------
    images : list
        A list of images representing the player's lives.

    Methods
    -------
    remove_image()
        Removes one life image from the beginning of the self.images list.
    reset_lives(numlives)
        Resets the self.images list based on the number of lives provided.
    get_image(x, y)
        Gets the image at the specified x and y coordinates.
    """

    def __init__(self, numlives: int) -> None:
        """
        Calls the initialization method of the parent Spritesheet class.

        Initializes the images representing the player's lives using the
        reset_lives method.

        Parameters
        ----------
        numlives : int
            The number of lives to represent.
        """
        Spritesheet.__init__(self)
        self.reset_lives(numlives)

    def remove_image(self) -> None:
        """
        Removes one life image from the beginning of the self.images list.
        """
        if len(self.images) > 0:
            self.images.pop(0)

    def reset_lives(self, numlives: int) -> None:
        """
        Resets the self.images list based on the number of lives provided.
        Each life is represented by an image, and the method populates the list
        with the appropriate number of life images.

        Parameters
        ----------
        numlives : int
            The number of lives to represent.
        """
        self.images = []
        for i in range(numlives):
            self.images.append(self.get_image(0, 0))

    def get_image(self, x: int, y: int) -> pygame.Surface:
        """
        Overrides the get_image method from the parent Spritesheet class to
        always retrieve a sprite of size 2 * TILEWIDTH by 2 * TILEHEIGHT.

        Parameters
        ----------
        x : int
            The x-coordinate of the sprite to retrieve from the sprite sheet.
        y : int
            The y-coordinate of the sprite to retrieve from the sprite sheet.

        Returns
        -------
        pygame.Surface
            The sprite at the specified x and y coordinates.
        """
        return Spritesheet.get_image(self, x, y, 2 * TILEWIDTH, 2 * TILEHEIGHT)


class MazeSprites(Spritesheet):
    """
    handle the sprites representing the maze layout in the Pac-Man game.

    Attributes
    ----------
    data : np.ndarray
        A NumPy array of strings representing the maze layout.
    rotdata : np.ndarray
        A NumPy array of strings representing the rotation data for the maze layout.

    Methods
    -------
    read_maze_file(mazefile)
        Reads the maze layout from a file and returns it as a NumPy array of strings.
    construct_background(background, y)
        Constructs the maze background by iterating over the maze data (self.data).
    rotate(sprite, value)
        Rotates the provided sprite by a specified angle.
    """

    def __init__(self) -> None:
        """
        Calls the initialization method of the parent Spritesheet class.

        Reads the maze layout from a file (mazefile) and stores it in self.data.

        Reads the rotation data for the maze layout from another file (rotfile)
        and stores it in self.rotdata.

        Parameters
        ----------
        mazefile : str
            The name of the file to read the maze layout from.
        rotfile : str
            The name of the file to read the rotation data from.
        """
        mazefile = "dooders/game/assets/maze1.txt"
        rotfile = "dooders/game/assets/maze1_rotation.txt"
        Spritesheet.__init__(self)
        self.data = self.read_maze_file(mazefile)
        self.rotdata = self.read_maze_file(rotfile)

    def get_image(self, x: int, y: int) -> pygame.Surface:
        """
        Overrides the get_image method from the parent Spritesheet class to
        always retrieve a sprite of size TILEWIDTH by TILEHEIGHT.

        Parameters
        ----------
        x : int
            The x-coordinate of the sprite to retrieve from the sprite sheet.
        y : int
            The y-coordinate of the sprite to retrieve from the sprite sheet.

        Returns
        -------
        pygame.Surface
            The sprite at the specified x and y coordinates.
        """
        return Spritesheet.get_image(self, x, y, TILEWIDTH, TILEHEIGHT)

    def read_maze_file(self, mazefile: str) -> np.ndarray:
        """
        Reads the maze layout from a file and returns it as a NumPy array of strings.

        Parameters
        ----------
        mazefile : str
            The name of the file to read the maze layout from.

        Returns
        -------
        np.ndarray
            A NumPy array of strings representing the maze layout.
        """
        # print(f'Loading maze file "{mazefile}"')
        return np.loadtxt(mazefile, dtype="<U1")

    def construct_background(
        self, background: pygame.Surface, y: int
    ) -> pygame.Surface:
        """
        Constructs the maze background by iterating over the maze data (self.data).

        For each cell in the maze data, it checks if the cell contains a digit
        (indicating a specific sprite) or an "=" (indicating a specific sprite).

        It then retrieves the appropriate sprite, rotates it based on the
        rotation data (self.rotdata), and blits (draws) it onto the provided
        background surface.

        Parameters
        ----------
        background : pygame.Surface
            The surface to draw the maze background on.
        y : int
            The y-coordinate of the sprite to retrieve from the sprite sheet.

        Returns
        -------
        pygame.Surface
            The background surface with the maze drawn on it.
        """
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                # print(f"row: {row}, col: {col}, data: {self.data[row][col]}")
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    # print(f"row: {row}, col: {col}, x: {x}, y: {y}")
                    sprite = self.get_image(x, y)
                    # print(sprite)
                    rotval = int(self.rotdata[row][col])
                    sprite = self.rotate(sprite, rotval)
                    background.blit(sprite, (col * TILEWIDTH, row * TILEHEIGHT))
                elif self.data[row][col] == "=":
                    sprite = self.get_image(10, 8)
                    background.blit(sprite, (col * TILEWIDTH, row * TILEHEIGHT))

        # print("********************************")

        return background

    def rotate(self, sprite: pygame.surface, value: int) -> pygame.Surface:
        """
        Rotates the provided sprite by a specified angle.

        The angle is calculated as value * 90, so the value should be in the
        range [0, 3] to represent the four possible rotations
        (0°, 90°, 180°, and 270°).

        Parameters
        ----------
        sprite : pygame.Surface
            The sprite to rotate.
        value : int
            The number of 90° rotations to perform.

        Returns
        -------
        pygame.Surface
            The rotated sprite.
        """
        return pygame.transform.rotate(sprite, value * 90)
