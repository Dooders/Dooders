"""
Space: Graph
------------
"""

from functools import singledispatchmethod
import networkx as nx
import matplotlib.pyplot as plt
from typing import Any, Dict, Iterator, List, Sequence, Tuple, Union, cast

from dooders.sdk.modules.space import Space

X = int
Y = int
Coordinate = Tuple[X, Y]


class Graph:
    """
    A graph is a collection of nodes (vertices) along with identified pairs of nodes (called edges, links, etc).

    Parameters
    ----------
    settings: dict, {torus: bool, width: int, height: int}
        A dictionary of settings for the grid.
        The following settings are available:
        torus: bool, default: True
            A boolean indicating if the grid is a torus.
            Torus grids wrap around the edges.
        width: int, default: 10
            The width of the grid.
        height: int, default: 10
            The height of the grid.

    Attributes
    ----------
    torus: bool
        See settings.
    width: int
        See settings.
    height: int
        See settings.
    _graph: nx.Graph
        The graph object.
    _object_index: Dict[str, Coordinate]
        A dictionary mapping object names to coordinates.

    Methods
    -------
    create_grid_graph()
        Creates a grid graph.
    get_neighbors(node_number)
        Returns the neighbors of a node.
    """

    _graph: nx.Graph
    _object_index: Dict[str, Coordinate]

    def __init__(self, settings: dict = {}) -> None:
        self.torus = settings.get("torus", False)
        self.height = settings.get("height", 10)
        self.width = settings.get("width", 10)
        self._graph = self._build()

    def _build(self) -> nx.Graph:
        """
        Creates a grid graph.

        Returns
        -------
        G: nx.Graph
            A grid graph based on the settings (torus, width, height)
        """
        G = nx.grid_2d_graph(self.height, self.width)

        for node in G.nodes():
            G.nodes[node]["space"] = Space(self.width, self.height)

        if self.torus:
            for x in range(self.height):
                G.add_edge((x, 0), (x, self.width - 1))
            for y in range(self.width):
                G.add_edge((0, y), (self.height - 1, y))

        # Label nodes with integers instead of (x, y) coordinates
        relabel_dict = {(x, y): y * self.width + x for x, y in G.nodes()}
        G = nx.relabel_nodes(G, relabel_dict)

        return G

    def coordinate_to_node_label(self, x: "X", y: "Y") -> int:
        """
        Converts a coordinate to a node label.

        Parameters
        ----------
        x: int
            The x coordinate.
        y: int
            The y coordinate.

        Returns
        -------
        node_label: int
            The node label. Example: (0, 0) -> 0, (0, 1) -> 10,
            (1, 0) -> 1, (1, 1) -> 11
        """
        return y * self.width + x

    def add(self, object: object, coordinate: Coordinate) -> None:
        """
        Adds an object to the graph and updates the object index.

        Parameters
        ----------
        object: object
            The object to add.
        coordinate: Coordinate
            The coordinate to add the object to.
        """
        node_label = self.coordinate_to_node_label(*coordinate)
        node = self._graph.nodes[node_label]
        node.space.add(object)
        self._object_index[object.id] = coordinate
        object.position = coordinate

    @singledispatchmethod
    def remove(self, type: Union[object, str]) -> None:
        raise NotImplementedError(
            "You must pass either an object or an object id to remove."
        )

    @remove.register
    def _(self, object: object) -> None:
        """
        Removes an object from the graph and updates the object index.

        Parameters
        ----------
        object: object
            The object to remove.
        """
        node_label = self.coordinate_to_node_label(*object.position)
        node = self._graph.nodes[node_label]
        node.space.remove(object)
        self._object_index.pop(object.id)

    @remove.register
    def _(self, object_id: str) -> None:
        """
        Removes an object from the graph and updates the object index.

        Parameters
        ----------
        object_id: str
            The object id to remove.
        """
        coordinate = self._object_index[object_id]
        node_label = self.coordinate_to_node_label(*coordinate)
        node = self._graph.nodes[node_label]
        node.space.remove(object_id)
        self._object_index.pop(object_id)

    def coordinates(self) -> Iterator[Coordinate]:
        """
        Return an iterator over all coordinates in the grid.

        Returns
        -------
        Iterator[Coordinate]
            An iterator over all coordinates in the grid.
            Example: [(0, 0), (0, 1), (0, 2), (0, 3)]

        Example
        -------
        for coordinate in grid.coordinates():
            print(coordinate)
        >>> (0, 0)
        >>> (0, 1)
        >>> (0, 2)
        """
        for node in self._graph.nodes:
            yield self._graph.nodes[node]["space"].coordinate

    def spaces(self) -> Iterator[Space]:
        """
        Return an iterator over all spaces in the grid.

        Returns
        -------
        Iterator[Space]
            An iterator over all spaces in the grid.
            Example: [Space(0, 0), Space(0, 1), Space(0, 2), Space(0, 3)]

        Example
        -------
        for space in grid.spaces():
            print(space)
        >>> Space(0, 0)
        >>> Space(0, 1)
        >>> Space(0, 2)
        """
        for node in self._graph.nodes:
            yield self._graph.nodes[node]["space"]

    @singledispatchmethod
    def contents(self, object_type: str = None) -> Iterator[Any]:
        """
        Return an iterator over all contents in the grid.

        With no arguments, it will return all contents.
        Include an object type to return only that type of object.

        Parameters
        ----------
        type: Any, optional
            The type of contents to return. Defaults to all.
            object types include 'Dooder', 'Energy', etc.

        Returns
        -------
        Iterator[Any], [<Dooder>, <Energy>, <Dooder>, <Energy>]
            An iterator over all contents in the grid.

        Example
        -------
        for object in grid.contents():
            print(object)
        >>> <Dooder>
        >>> <Energy>
        >>> <Dooder>
        """
        for space in self.spaces():
            for object in space.contents():
                if object_type is None or isinstance(object, object_type):
                    yield object

    @contents.register
    def _(self, position: tuple) -> Iterator[Any]:
        """
        Return an iterator over all contents in a Space on the grid.

        Parameters
        ----------
        position: Coordinate, (int, int)
            The position to get the contents from.

        Returns
        -------
        Iterator[Any], [<Dooder>, <Energy>, <Dooder>, <Energy>]
            An iterator over all contents in a Space on the grid.

        Example
        -------
        for object in grid.contents((0, 0)):
            print(object)
        >>> <Dooder>
        >>> <Energy>
        >>> <Dooder>
        """
        node_label = self.coordinate_to_node_label(*position)
        for object in self._graph.nodes[node_label]["space"].contents():
            yield object

    def get_neighbors(self, node_label: int) -> List[int]:
        """
        Returns the neighbors of a node.

        Parameters
        ----------
        node_label: int
            The node label.

        Returns
        -------
        neighbor_nodes: List[int]
            A list of neighbor nodes.
        """
        neighbor_nodes = list(self._graph.neighbors(node_label))
        return neighbor_nodes
