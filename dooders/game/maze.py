from abc import ABC
from typing import TYPE_CHECKING

from dooders.game.constants import *


class MazeBase(ABC):
    """
    Base class for mazes. This class is not meant to be instantiated directly.

    Attributes
    ----------
    name : str
        The name of the maze.
    portalPairs : dict
        A dictionary of portal pairs. The key is the portal pair number, and
        the value is a tuple of the two portal locations.
    homeoffset : tuple
        The offset of the home nodes from the maze nodes.
    homenodeconnectLeft : tuple
        The location of the left home node.
    homenodeconnectRight : tuple
        The location of the right home node.
    pacmanStart : tuple
        The location of the pacman start node.
    fruitStart : tuple
        The location of the fruit start node.
    ghostNodeDeny : dict
        A dictionary of ghost node deny lists. The key is the direction, and the
        value is a list of tuples of the locations of the nodes to deny access to.

    Methods
    -------
    set_portal_pairs(nodes)
        Sets the portal pairs in the nodes object.
    connect_home_nodes(nodes)
        Connects the home nodes in the nodes object.
    add_offset(x, y)
        Adds the home offset to the given coordinates.
    deny_ghosts_access(ghosts, nodes)
        Denies the ghosts access to the home nodes.
    """

    def __init__(self) -> None:
        self.portalPairs = {}
        self.homeoffset = (0, 0)
        self.ghostNodeDeny = {UP: (), DOWN: (), LEFT: (), RIGHT: ()}

    def set_portal_pairs(self, nodes: "Node") -> None:
        """
        Takes a nodes argument and sets the portal pairs in the nodes object.

        Iterates through the portal pairs stored in the portalPairs dictionary
        and sets these portal pairs in the nodes object.

        Parameters
        ----------
        nodes : Node
            The nodes object to set the portal pairs in.
        """
        for pair in list(self.portalPairs.values()):
            nodes.set_portal_pair(*pair)

    def connect_home_nodes(self, nodes: "Node") -> None:
        """
        Creates home nodes with an offset specified by homeoffset using the
        create_home_nodes method of the nodes object.

        Connects the newly created home nodes to other nodes using the
        connect_home_nodes method of the nodes object, based on directions
        specified by homenodeconnectLeft and homenodeconnectRight.

        Parameters
        ----------
        nodes : Node
            The nodes object to create the home nodes in.
        """
        key = nodes.create_home_nodes(*self.homeoffset)
        nodes.connect_home_nodes(key, self.homenodeconnectLeft, LEFT)
        nodes.connect_home_nodes(key, self.homenodeconnectRight, RIGHT)

    def add_offset(self, x: int, y: int) -> tuple:
        """
        Returns a new tuple by adding x to the first element and y to the second
        element of the homeoffset tuple.

        This is used to calculate positions with an offset relative to the home nodes.

        Parameters
        ----------
        x : int
            The x offset.
        y : int
            The y offset.

        Returns
        -------
        tuple
            The new tuple with the offset added.
        """
        return x + self.homeoffset[0], y + self.homeoffset[1]

    def deny_ghosts_access(self, ghosts: "Ghost", nodes: "Node") -> None:
        """
        Adds denial rules to restrict ghost access in certain directions for
        nodes in the maze environment.

        Specifically, it denies access for ghosts to certain positions with
        offsets and directions specified in ghostNodeDeny.

        Parameters
        ----------
        ghosts : Ghost
            The ghosts object to deny access to.
        nodes : Node
            The nodes object to deny access in.
        """
        nodes.deny_access_list(*(self.add_offset(2, 3) + (LEFT, ghosts)))
        nodes.deny_access_list(*(self.add_offset(2, 3) + (RIGHT, ghosts)))

        for direction in list(self.ghostNodeDeny.keys()):
            for values in self.ghostNodeDeny[direction]:
                nodes.deny_access_list(*(values + (direction, ghosts)))


class Maze1(MazeBase):
    """
    The first maze in the game.

    Attributes
    ----------
    name : str
        The name of the maze.
    portalPairs : dict
        A dictionary of portal pairs. The key is the portal pair number, and
        the value is a tuple of the two portal locations.
    homeoffset : tuple
        The offset of the home nodes from the maze nodes.
    homenodeconnectLeft : tuple
        The location of the left home node.
    homenodeconnectRight : tuple
        The location of the right home node.
    pacmanStart : tuple
        The location of the pacman start node.
    fruitStart : tuple
        The location of the fruit start node.
    ghostNodeDeny : dict
        A dictionary of ghost node deny lists. The key is the direction, and the
        value is a list of tuples of the locations of the nodes to deny access to.
    """

    def __init__(self):
        MazeBase.__init__(self)
        self.name = "maze1"
        self.portalPairs = {0: ((0, 17), (27, 17))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (12, 14)
        self.homenodeconnectRight = (15, 14)
        self.pacmanStart = (15, 26)
        self.fruitStart = (9, 20)
        self.ghostNodeDeny = {
            UP: ((12, 14), (15, 14), (12, 26), (15, 26)),
            LEFT: (self.add_offset(2, 3),),
            RIGHT: (self.add_offset(2, 3),),
        }


class Maze2(MazeBase):
    """
    The second maze in the game.

    Attributes
    ----------
    name : str
        The name of the maze.
    portalPairs : dict
        A dictionary of portal pairs. The key is the portal pair number, and
        the value is a tuple of the two portal locations.
    homeoffset : tuple
        The offset of the home nodes from the maze nodes.
    homenodeconnectLeft : tuple
        The location of the left home node.
    homenodeconnectRight : tuple
        The location of the right home node.
    pacmanStart : tuple
        The location of the pacman start node.
    fruitStart : tuple
        The location of the fruit start node.
    ghostNodeDeny : dict
        A dictionary of ghost node deny lists. The key is the direction, and the
        value is a list of tuples of the locations of the nodes to deny access to.
    """

    def __init__(self):
        MazeBase.__init__(self)
        self.name = "maze2"
        self.portalPairs = {0: ((0, 4), (27, 4)), 1: ((0, 26), (27, 26))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (9, 14)
        self.homenodeconnectRight = (18, 14)
        self.pacmanStart = (16, 26)
        self.fruitStart = (11, 20)
        self.ghostNodeDeny = {
            UP: ((9, 14), (18, 14), (11, 23), (16, 23)),
            LEFT: (self.add_offset(2, 3),),
            RIGHT: (self.add_offset(2, 3),),
        }


class MazeData:
    """
    Class to load mazes.

    Attributes
    ----------
    obj : MazeBase
        The maze object.
    mazedict : dict
        A dictionary of mazes. The key is the level number, and the value is the
        maze object.

    Methods
    -------
    load_maze(level)
        Loads the maze for the given level.
    """

    def __init__(self):
        self.obj = None
        self.mazedict = {0: Maze1, 1: Maze2}

    def load_maze(self, level: int) -> None:
        """
        Loads the maze for the given level and stores it in the obj attribute.

        Parameters
        ----------
        level : int
            The level number. (0 or 1)
        """
        self.obj = self.mazedict[level % len(self.mazedict)]()
