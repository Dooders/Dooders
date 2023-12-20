from typing import TYPE_CHECKING, List

from dooders.games.pacman.settings import MapLegend
from dooders.games.pacman.sprites import MapSprites
from dooders.sdk.surfaces.graph import Graph

if TYPE_CHECKING:
    from dooders.games.npc import NPC
    from dooders.sdk.base.coordinate import Coordinate


class Map:
    """
    The map of the game

    Attributes
    ----------
    sprites : MapSprites
        The sprites of the map
    graph : Graph
        The graph of the map

    Methods
    -------
    add(sprite, coordinates)
        Add a sprite to the map
    remove(entity)
        Remove a sprite from the map
    path_finding(start, end)
        Find the path between two coordinates
    _build_graph()
        Build the graph of the map via networkx
    """

    def __init__(self) -> None:
        """
        Responsible for loading the map and building the graph

        Attributes
        ----------
        sprites : MapSprites
            The sprites of the map
        graph : Graph
            The graph of the map
        """
        self.sprites = MapSprites()
        self.graph = self._build_graph()

    def add(self, sprite: "NPC", coordinates: "Coordinate") -> None:
        """
        Add a sprite to the map

        Parameters
        ----------
        sprite : NPC
            The sprite to add
        coordinates : Coordinate
            The coordinates of the sprite
        """
        self.graph.add(sprite, coordinates)

    def remove(self, entity: "NPC") -> None:
        """
        Remove a sprite from the map

        Parameters
        ----------
        entity : NPC
            The sprite to remove
        """
        self.graph.remove(entity)

    def path_finding(
        self, start: "Coordinate", end: "Coordinate"
    ) -> List["Coordinate"]:
        """
        Find the path between two coordinates

        Parameters
        ----------
        start : Coordinate
            The start coordinate
        end : Coordinate
            The end coordinate

        Returns
        -------
        List[Coordinate]
            The path between the two coordinates
        """
        return self.graph.path_finding(start, end)

    def _build_graph(self) -> "Graph":
        """
        Build the graph of the map via networkx

        Returns
        -------
        Graph
            The graph of the map
            
        See Also
        --------
        dooders.sdk.surfaces.graph.Graph
        """
        map_data = self.sprites.data
        grid_height = len(map_data)
        grid_width = len(map_data[0])
        graph = Graph({"height": grid_height, "width": grid_width, "map": map_data})

        nodes_to_remove = []

        for space in graph.spaces():
            if space.tile_type in MapLegend.PLAYABLE:
                space.playable = True
            else:
                nodes_to_remove.append(space.coordinates)

        # Removing the nodes that are not playable
        for node in nodes_to_remove:
            graph._graph.remove_node(node)

        return graph
