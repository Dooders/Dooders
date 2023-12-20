from abc import ABC

import pygame

from dooders.games.pacman.settings import *
from dooders.sdk.base.coordinate import Coordinate


class Text(ABC):
    """
    This class provides a convenient way to display text elements within a game.

    It handles the rendering of the text, updating its state based on time,
    and managing its visibility and lifespan.

    Attributes
    ----------
    id : int
        The id of the text.
    text : str
        The text content.
    color : tuple
        The color of the text.
    size : int
        The size of the text.
    visible : bool
        The visibility of the text.
    position : Coordinate
        The position of the text.
    timer : int
        The timer for the text.
    lifespan : int
        The lifespan of the text.
    label : pygame.Surface
        The rendered version of the text.
    destroy : bool
        The flag that indicates whether the text should be destroyed.
    font : pygame.font.Font
        The font used to render the text.

    Methods
    -------
    setup_font(font_path: str) -> None
        Initializes the font for rendering the text using a specified font
        path and size.
    create_label() -> None
        Renders the text content into a label using the specified font and color.
    set_text(new_text: str) -> None
        Updates the text content and recreates the label.
    update(dt: float) -> None
        If the text object has a lifespan, this method updates a timer based on
        the time delta (dt).
    render(screen: pygame.Surface) -> None
        Renders the text label onto the provided screen (or surface) if the
        text object is visible.
    """

    def __init__(
        self,
        text: str,
        color,
        x: int,
        y: int,
        size: int,
        time: int = None,
        id: int = None,
        visible: bool = True,
    ) -> None:
        """
        Initializes the text object with various attributes like the text content,
        color, position (x, y), size, and optional attributes like time (lifespan),
        id, and visibility.

        The lifespan attribute indicates how long the text should be displayed
        before it's destroyed.

        The destroy attribute is a flag that indicates whether the text object
        should be destroyed (removed from the game).

        Sets up the font for rendering the text using the setup_font method.

        Creates a label (a rendered version of the text) using the
        create_label method.

        Parameters
        ----------
        text : str
            The text content.
        color : tuple
            The color of the text.
        x : int
            The x position of the text.
        y : int
            The y position of the text.
        size : int
            The size of the text.
        time : int, optional
            The lifespan of the text. The default is None.
        id : int, optional
            The id of the text. The default is None.
        visible : bool, optional
            The visibility of the text. The default is True.
        """
        self.id = id
        self.text = text
        self.color = color.value if isinstance(color, Colors) else color
        self.size = size
        self.visible = visible
        self.position = Coordinate(x, y)
        self.timer = 0
        self.lifespan = time
        self.label = None
        self.destroy = False
        self.setup_font("dooders/games/pacman/assets/PressStart2P-Regular.ttf")
        self.create_label()

    def setup_font(self, font_path: str) -> None:
        """
        Initializes the font for rendering the text using a specified font
        path and size.

        Parameters
        ----------
        font_path : str
            The path to the font file.
        """
        self.font = pygame.font.Font(font_path, self.size)

    def create_label(self) -> None:
        """
        Renders the text content into a label using the specified font and color.
        """
        self.label = self.font.render(self.text, 1, self.color)

    def set_text(self, new_text: str) -> None:
        """
        Updates the text content and recreates the label.

        Parameters
        ----------
        new_text : str
            The new text content.
        """
        self.text = str(new_text)
        self.create_label()

    def update(self, dt: float) -> None:
        """
        If the text object has a lifespan, this method updates a timer based on
        the time delta (dt).
        When the timer exceeds the lifespan, the text object is marked f
        or destruction.

        Parameters
        ----------
        dt : float
            The time delta.
        """
        if self.lifespan is not None:
            self.timer += dt
            if self.timer >= self.lifespan:
                self.timer = 0
                self.lifespan = None
                self.destroy = True

    def render(self, screen: pygame.Surface) -> None:
        """
        Renders the text label onto the provided screen (or surface) if the
        text object is visible.

        Parameters
        ----------
        screen : pygame.Surface
            The surface to render the text label onto.
        """
        if self.visible:
            x, y = self.position.as_tuple()
            screen.blit(self.label, (x, y))


class TextGroup(ABC):
    """ """

    def __init__(self) -> None:
        """
        Initializes the next available ID for text elements.

        Initializes an empty dictionary alltext to store all the text elements.

        Sets up predefined text elements using the setup_text method.

        Shows the "READY!" text by default.
        """
        self.nextid = 10
        self.alltext = {}
        self.setup_text()
        self.show_text(Texts.READYTXT)

    def add_text(
        self,
        text: str,
        color: tuple,
        x: int,
        y: int,
        size: int,
        time: int = None,
        id: str = None,
    ) -> int:
        """
        Adds a new Text object to the alltext dictionary with a unique ID
        and returns the ID.

        Parameters
        ----------
        text : str
            The text content.
        color : tuple
            The color of the text.
        x : int
            The x position of the text.
        y : int
            The y position of the text.
        size : int
            The size of the text.
        time : int, optional
            The lifespan of the text. The default is None.
        id : int, optional
            The id of the text. The default is None.

        Returns
        -------
        int
            The id of the text.
        """
        self.nextid += 1
        self.alltext[self.nextid] = Text(text, color, x, y, size, time=time, id=id)
        return self.nextid

    def remove_text(self, id):
        self.alltext.pop(id)

    def setup_text(self):
        size = Dimensions.TILEHEIGHT
        self.alltext[Texts.SCORETXT] = Text(
            "0".zfill(8), Colors.WHITE.value, 0, Dimensions.TILEHEIGHT, size
        )
        self.alltext[Texts.LEVELTXT] = Text(
            str(1).zfill(3),
            Colors.WHITE,
            23 * Dimensions.TILEWIDTH,
            Dimensions.TILEHEIGHT,
            size,
        )
        self.alltext[Texts.READYTXT] = Text(
            "READY!",
            Colors.YELLOW.value,
            11.25 * Dimensions.TILEWIDTH,
            20 * Dimensions.TILEHEIGHT,
            size,
            visible=False,
        )
        self.alltext[Texts.PAUSETXT] = Text(
            "PAUSED!",
            Colors.YELLOW.value,
            10.625 * Dimensions.TILEWIDTH,
            20 * Dimensions.TILEHEIGHT,
            size,
            visible=False,
        )
        self.alltext[Texts.GAMEOVERTXT] = Text(
            "GAMEOVER!",
            Colors.YELLOW.value,
            10 * Dimensions.TILEWIDTH,
            20 * Dimensions.TILEHEIGHT,
            size,
            visible=False,
        )
        self.add_text("SCORE", Colors.WHITE.value, 0, 0, size)
        self.add_text("LEVEL", Colors.WHITE.value, 23 * Dimensions.TILEWIDTH, 0, size)

    def update(self, dt):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].update(dt)
            if self.alltext[tkey].destroy:
                self.remove_text(tkey)

    def show_text(self, id):
        self.hide_text()
        self.alltext[id].visible = True

    def hide_text(self):
        self.alltext[Texts.READYTXT].visible = False
        self.alltext[Texts.PAUSETXT].visible = False
        self.alltext[Texts.GAMEOVERTXT].visible = False

    def update_score(self, score):
        self.update_text(Texts.SCORETXT, str(score).zfill(8))

    def update_level(self, level):
        self.update_text(Texts.LEVELTXT, str(level + 1).zfill(3))

    def update_text(self, id, value):
        if id in self.alltext.keys():
            self.alltext[id].set_text(value)

    def render(self, screen):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].render(screen)
