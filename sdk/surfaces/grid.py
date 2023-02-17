import itertools
from functools import singledispatchmethod
from typing import Any, Dict, Iterator, List, Sequence, Tuple, Union, cast

from sdk.modules.space import Space
from sdk.utils.types import UniqueID

GridRow = List[Space]
X = int
Y = int
Coordinate = Tuple[X, Y]

#! this will inherit surface???
#! change unique_id attribute to just id
#! make id creator class


class Grid:
    """
    A rectangular grid of Spaces.

    Parameters
    ----------
    settings: dict
        A dictionary of settings for the grid.
        The following settings are available:
        torus: bool
            A boolean indicating if the grid is a torus.
            Default: True
        width: int
            The width of the grid.
            Default: 10
        height: int
            The height of the grid.
            Default: 10

    Methods
    -------
    add(object: object, coordinate: Coordinate) -> None
        Add an object to a space on the grid.
    remove(object: object) -> None
        Remove an object from the grid.
    remove(object_id: UniqueID) -> None
        Remove an object from the grid based on its id.
    coordinates() -> Iterator[Coordinate]
        Return an iterator over all coordinates in the grid.
    spaces() -> Iterator[Space]
        Return an iterator over all spaces in the grid.
    contents() -> Iterator[object]
        Return an iterator over all objects in the grid.
    nearby_spaces(coordinate: Coordinate, radius: int) -> Iterator[Space]
        Return an iterator over all spaces within a radius of a coordinate.
    nearby_contents(coordinate: Coordinate, radius: int) -> Iterator[object]
        Return an iterator over all objects within a radius of a coordinate.
    nearby_coordinates(coordinate: Coordinate, radius: int) -> Iterator[Coordinate]
        Return an iterator over all coordinates within a radius of a coordinate.

    See Also
    --------
    sdk.modules.space.Space
    """
    _grid: List[List[GridRow]]
    _object_index: Dict[UniqueID, Coordinate]

    def __init__(self, settings: dict) -> None:
        self.torus = settings.get('torus', True)
        self.width = settings.get('width', 10)
        self.height = settings.get('height', 10)

        self._grid = []
        self._object_index = {}
        self._nearby_cache = {}

        self._build()

    def _build(self) -> None:
        """
        Builds the grid based on the provided settings.
        """
        for x in range(self.width):
            col = []
            for y in range(self.height):
                space = Space(x, y)
                col.append(space)
            self._grid.append(col)

    def add(self, object: object, coordinate: Coordinate) -> None:
        """
        Add an object to a space on the grid.

        Parameters
        ----------
        object: object
            The object to add to the grid (Dooder, Energy, etc.).
        coordinate: Coordinate
            Where to place the object. 
        """
        x, y = coordinate
        space = self._grid[x][y]
        space.add(object)
        self._object_index[object.id] = coordinate
        object.position = coordinate

    @singledispatchmethod
    def remove(self, type: Union[object, str]) -> None:
        """
        Remove content from a Space on the grid.

        Must be an object or an objects UniqueID

        Parameters
        ----------
        type: Union[object, UniqueID]
            The object or id of the object to remove. 
            It will also be removed from the object index.
        """
        raise NotImplementedError(
            "You must pass either an object or an object id to remove.")

    @remove.register
    def _(self, object: object) -> None:
        """
        Remove content from a Space on the grid based on the provided object.

        Parameters
        ----------
        object: object
            The object to remove. 
            It will also be removed from the object index.
        """
        x, y = object.position
        self._grid[x][y].remove(object)
        self._object_index.pop(object.id)

    @remove.register
    def _(self, object_id: str) -> None:
        """
        Remove content from a Space on the grid based on the object id.

        Parameters
        ----------
        object_id: UniqueID
            The id of the object to remove. 
            It will also be removed from the object index.
        """
        x, y = self._object_index[object_id]
        self._grid[x][y].remove(object_id)
        self._object_index.pop(object_id)

    def coordinates(self) -> Iterator[Coordinate]:
        """
        Return an iterator over all coordinates in the grid.

        Returns
        -------
        Iterator[Coordinate]
            An iterator over all coordinates in the grid.
            Example: [(0, 0), (0, 1), (0, 2), (0, 3)]
        """
        for row in self._grid:
            for space in row:
                yield space.coordinates

    def spaces(self) -> Iterator[Space]:
        """
        Return an iterator over all Spaces in the grid.

        Returns
        -------
        Iterator[Location]
            An iterator over all Spaces in the grid.
            Example: [<Space>, <Space>, <Space>, <Space>]
        """
        for row in self._grid:
            for space in row:
                yield space

    def contents(self, object_type: str = None) -> Iterator[Any]:
        """
        Return an iterator over all contents in the grid.

        With no arguments, it will return all contents.
        Include an object type to return only that type of object.

        Parameters
        ----------
        type: Any
            The type of contents to return. Defaults to all.
            object types include 'Dooder', 'Energy', etc.

        Returns
        -------
        Iterator[Any]
            An iterator over all contents in the grid. 
            Example: [<Dooder>, <Energy>, <Dooder>, <Energy>]
        """
        for row in self._grid:
            for space in row:
                for object in space.contents.values():
                    if object_type is None:
                        yield object
                    if object.__class__.__name__ == object_type:
                        yield object

    def nearby_spaces(
        self,
        position: Coordinate,
        moore: bool = True,
        include_center: bool = False,
        radius: int = 1
    ) -> Iterator[Space]:
        """
        Return an iterator of Spaces nearby a given position.

        Parameters
        ----------
        position: Coordinate
            The position to get the nearby spaces from.
        moore: bool
            A boolean indicating if the neighborhood should be Moore or Von Neumann.
            Default: True
        include_center: bool
            A boolean indicating if the center position should be included in the neighborhood.
            Default: False
        radius: int
            The radius of the neighborhood. Default: 1

        Returns
        -------
        Iterator[Space]
            An iterator of Spaces nearby a given position.
            Example: [<Space>, <Space>, <Space>, <Space>]
        """
        nearby = self.nearby_coordinates(
            position, moore, include_center, radius)
        return [self._grid[pos[0]][pos[1]] for pos in nearby]

    def nearby_contents(
        self,
        position: Coordinate,
        moore: bool = True,
        include_center: bool = False,
        radius: int = 1
    ) -> Iterator[Any]:
        """
        Return an iterator of contents nearby a given position.

        Parameters
        ----------
        position: Coordinate
            The position to get the nearby contents from.
        moore: bool
            A boolean indicating if the neighborhood should be Moore or Von Neumann.
            Default: True
        include_center: bool
            A boolean indicating if the center position should be included in the neighborhood.
            Default: False
        radius: int
            The radius of the neighborhood. Default: 1

        Returns
        -------
        Iterator[Any]
            An iterator of contents nearby a given position.
            Example: [<Dooder>, <Energy>, <Dooder>, <Dooder>]
        """
        nearby_contents = self.nearby_coordinates(
            position, moore, include_center, radius)
        return [self._grid[pos[0]][pos[1]].contents for pos in nearby_contents]

    def nearby_coordinates(
        self,
        position: Coordinate,
        moore: bool = True,
        include_center: bool = False,
        radius: int = 1
    ) -> Iterator[Coordinate]:
        """
        Return an iterator of coordinates nearby a given position.

        Parameters
        ----------
        position: Coordinate
            The position to get the nearby coordinates from.
            Example: (0, 0)
        moore: bool
            A boolean indicating if the neighborhood should be Moore or Von Neumann.
            Default: True
        include_center: bool
            A boolean indicating if the center position should be included in the neighborhood.
            Default: False
        radius: int
            The radius of the neighborhood. Default: 1

        Returns
        -------
        Iterator[Coordinate]
            An iterator of coordinates nearby a given position.
            Example: [(0, 0), (0, 1), (0, 2), (0, 3)]
        """
        cache_key = (position, moore, include_center, radius)
        nearby_coordinates = self._nearby_cache.get(cache_key, None)

        if nearby_coordinates is None:
            coordinates = []

            x, y = position
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if dx == 0 and dy == 0 and not include_center:
                        continue
                    # Skip coordinates that are outside manhattan distance
                    if not moore and abs(dx) + abs(dy) > radius:
                        continue

                    coord = (x + dx, y + dy)

                    if self.out_of_bounds(coord):
                        # Skip if not a torus and new coords out of bounds.
                        if not self.torus:
                            continue
                        coord = self.torus_adjustment(coord)

                    coordinates.append(coord)

            nearby_coordinates = coordinates
            self._nearby_cache[cache_key] = nearby_coordinates

        return nearby_coordinates

    def torus_adjustment(self, position: Coordinate) -> Coordinate:
        """
        Convert coordinate, handling torus looping.

        Parameters
        ----------
        position: Coordinate
            Coordinate tuple to convert.
            Example: (0, 0)

        Returns
        -------
        Coordinate
            Coordinate tuple adjusted for torus looping.
        """
        if not self.out_of_bounds(position):
            return position
        elif not self.torus:
            raise Exception("Point out of bounds, and space non-toroidal.")
        else:
            return position[0] % self.width, position[1] % self.height

    def out_of_bounds(self, position: Coordinate) -> bool:
        """
        Determines whether position is off the surface, returns the out of
        bounds coordinate.

        Parameters
        ----------
        position: Coordinate
            Coordinate tuple to check.

        Returns 
        -------
        bool
            True if position is off the surface, False otherwise.
        """
        x, y = position
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def __iter__(self) -> Iterator[GridRow]:
        """
        Create an iterator that chains the rows of the surface together
        as if it is one list.

        Returns
        -------
        Iterator[GridRow]
            The iterator of the surface.
        """
        return itertools.chain(*self._grid)

    @singledispatchmethod
    def __getitem__(self, value) -> Any:
        raise NotImplementedError(f'Type {type(value)} is unsupported')

    @__getitem__.register
    def _(self, value: int) -> GridRow:
        """ 
        Return the row at the given index.
        """
        return self._grid[value]

    @__getitem__.register
    def _(self, value: list) -> List[Space]:
        """ 
        Return the Spaces at the given coordinates.
        """
        index = cast(Sequence[Coordinate], value)

        cells = []
        for pos in index:
            x1, y1 = self.torus_adjustment(pos)
            cells.append(self._grid[x1][y1])
        return cells

    @__getitem__.register
    def _(self, value: tuple) -> Space:
        """ 
        Return the Space at the given coordinate.
        """
        index = cast(Coordinate, value)
        x, y = self.torus_adjustment(index)
        return self._grid[x][y]

    @__getitem__.register
    def _(self, value: str) -> Union[GridRow, List[Space], Space]:
        """ 
        Return the row at the given index or the Space at the given coordinate.
        """
        index = cast(str, value)
        if index == 'all':
            return self._grid
        else:
            for space in self.spaces():
                for objects in space.contents:
                    return space.contents.get(index, 'No object found')
