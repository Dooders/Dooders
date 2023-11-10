"""
Space: Graph
------------
"""

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
        self._object_index[object.name] = coordinate
        object.position = coordinate

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
        print(f"Neighbors of node {node_label}: {neighbor_nodes}")
        return neighbor_nodes


# Draw the graph with updated position mapping
# dim = 10
# pos = {(x + y * 10): (x, dim - 1 - y) for x in range(dim) for y in range(dim)}
# G = nx.grid_2d_graph(dim, dim)
# nx.draw(G, pos, with_labels=True, node_size=400, node_color="lightblue")
# plt.show()
