""" 
Space: Grid
-----------
Rectangular grid of Spaces.
"""

import itertools
from functools import singledispatchmethod
from typing import Any, Dict, Iterator, List, Sequence, Tuple, Union, cast

from dooders.sdk.modules.space import Space

GridRow = List[Space]
X = int
Y = int
Coordinate = Tuple[X, Y]


class Grid:
    """
    A rectangular grid of Spaces.

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

    Methods
    -------
    add(object: object, coordinate: Coordinate) -> None
        Add an object to a space on the grid based 
        on the provided coordinate.
    remove(object: object) -> None
        Remove an object from the grid.
    remove(object_id: str) -> None
        Remove an object from the grid based on its id.
    coordinates() -> Iterator[Coordinate]
        Return an iterator over all coordinates in the grid.
    spaces() -> Iterator[Space]
        Return an iterator over all spaces in the grid.
    contents() -> Iterator[object]
        Return an iterator over all objects in the grid.
    contents(object_type: str) -> Iterator[object]
        Return an iterator over all objects of a specific type in the grid.
    contents(coordinate: Coordinate) -> Iterator[object]
        Return an iterator over all objects in a specific space on the grid.
    nearby_spaces(coordinate: Coordinate, radius: int) -> Iterator[Space]
        Return an iterator over all spaces within a radius of a coordinate.
    nearby_contents(coordinate: Coordinate, radius: int) -> Iterator[object]
        Return an iterator over all objects within a radius of a coordinate.
    nearby_coordinates(coordinate: Coordinate, radius: int) -> Iterator[Coordinate]
        Return an iterator over all coordinates within a radius of a coordinate.

    See Also
    --------
    sdk.core.Space: A space on the grid.
    """
    _grid: List[List[GridRow]]
    _object_index: Dict[str, Coordinate]
    _nearby_cache: Dict[Coordinate, Dict[int, List[Coordinate]]]

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
        object: object, Dooder, Energy, etc.
            The object to add to the grid.
        coordinate: Coordinate, (int, int)
            Where to place the object. 

        Example
        -------
        grid.add(dooder, (0, 0))
        """
        x, y = coordinate
        space = self._grid[x][y]

        # Add the object to the space
        space.add(object)

        # Add the object to the object index for quick lookup
        self._object_index[object.id] = coordinate

        object.position = coordinate

    @singledispatchmethod
    def remove(self, type: Union[object, str]) -> None:
        """
        Remove content from a Space on the grid.

        Must pass an object or an object's id

        Parameters
        ----------
        type: Union[object, str]
            The object or id of the object to remove. 
            It will also be removed from the object index.

        Example
        -------
        grid.remove(dooder)
        grid.remove(dooder.id)
        """
        raise NotImplementedError(
            "You must pass either an object or an object id to remove.")

    @remove.register
    def _(self, object: object) -> None:
        """
        Remove content from a Space on the grid based on the provided object.

        Parameters
        ----------
        object: object, Dooder, Energy, etc.
            The object to remove. 
            It will also be removed from the object index.

        Example
        -------
        grid.remove(dooder)
        """
        x, y = object.position

        # Remove the object from the space
        # and the object index
        self._grid[x][y].remove(object)
        self._object_index.pop(object.id)

    @remove.register
    def _(self, object_id: str) -> None:
        """
        Remove content from a Space on the grid based on the object id.

        Parameters
        ----------
        object_id: str
            The id of the object to remove. 
            It will also be removed from the object index.

        Example
        -------
        grid.remove(dooder.id)
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

        Example
        -------
        for coordinate in grid.coordinates():
            print(coordinate)
        >>> (0, 0)
        >>> (0, 1)
        >>> (0, 2)
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

        Example
        -------
        for space in grid.spaces():
            print(space)
        >>> <Space>
        >>> <Space>
        >>> <Space>
        """
        for row in self._grid:
            for space in row:
                yield space

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
        for row in self._grid:
            for space in row:
                for object in space.contents.values():
                    if object_type is None:
                        yield object
                    if object.__class__.__name__ == object_type:
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
        x, y = position
        space = self._grid[x][y]
        for object in space.contents.values():
            yield object

    def nearby_spaces(
        self,
        position: Coordinate,
        moore: bool = True,
        include_center: bool = True,
        radius: int = 1
    ) -> Iterator[Space]:
        """
        Return an iterator of Spaces nearby a given position.

        Parameters
        ----------
        position: Coordinate, (int, int)
            The position to get the nearby spaces from.
        moore: bool, optional, default = True
            A boolean indicating if the perception 
            should be Moore or Von Neumann.
        include_center: bool, optional, default = True
            A boolean indicating if the center position 
            should be included in the perception.
        radius: int, default = 1
            The radius of the perception

        Returns
        -------
        Iterator[Space], [<Space>, <Space>, <Space>, <Space>]
            An iterator of Spaces nearby a given position.

        Example
        -------
        for space in grid.nearby_spaces((0, 0)):
            print(space)
        >>> <Space>
        >>> <Space>
        >>> <Space>
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
        position: Coordinate, (int, int)
            The position to get the nearby contents from.
        moore: bool, optional, default = True
            A boolean indicating if the perception 
            should be Moore or Von Neumann.
        include_center: bool, optional, default = False
            A boolean indicating if the center position 
            should be included in the perception.
        radius: int, optional, default = 1
            The radius of the perception.

        Returns
        -------
        Iterator[Any], [<Dooder>, <Energy>, <Dooder>, <Dooder>]
            An iterator of contents nearby a given position.

        Example
        -------
        for object in grid.nearby_contents((0, 0)):
            print(object)
        >>> <Dooder>
        >>> <Energy>
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
        position: Coordinate, (int, int)
            The position to get the nearby coordinates from.
        moore: bool, optional, default = True
            A boolean indicating if the perception 
            should be Moore or Von Neumann.
        include_center: bool, optional, default = False
            A boolean indicating if the center position 
            should be included in the perception.
        radius: int, optional, default = 1
            The radius of the perception.

        Returns
        -------
        Iterator[Coordinate], [(0, 0), (0, 1), (0, 2), (0, 3)]
            An iterator of coordinates nearby a given position.

        Example
        -------
        for coord in grid.nearby_coordinates((0, 0)):
            print(coord)
        >>> (0, 0)
        >>> (0, 1)
        >>> (0, 2)
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
        position: Coordinate, (int, int)
            Coordinate tuple to convert.

        Returns
        -------
        Coordinate, (int, int)
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
        position: Coordinate, (int, int)
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
        Iterator[GridRow], [<GridRow>, <GridRow>, <GridRow>, <GridRow>]
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

        Example
        -------
        grid[0]
        >>> <GridRow>
        """
        return self._grid[value]

    @__getitem__.register
    def _(self, value: list) -> List[Space]:
        """ 
        Return the Spaces at the given coordinates.

        Example
        -------
        grid[[(0, 0), (0, 1)]]
        >>> [<Space>, <Space>]
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

        Example
        -------
        grid[(0, 0)]
        >>> <Space>
        """
        index = cast(Coordinate, value)
        x, y = self.torus_adjustment(index)
        return self._grid[x][y]

    @__getitem__.register
    def _(self, value: str) -> Union[GridRow, List[Space], Space]:
        """ 
        Return the row at the given index or the Space at the given coordinate.

        Example
        -------
        grid['all']
        >>> [<GridRow>, <GridRow>, <GridRow>, <GridRow>]
        """
        index = cast(str, value)
        if index == 'all':
            return self._grid
        else:
            for space in self.spaces():
                for objects in space.contents:
                    return space.contents.get(index, 'No object found')

    @property
    def state(self) -> Dict:
        """
        Return the state of the grid.

        Returns
        -------
        Dict, {'width': 10, 'height': 10, 'torus': False}
            The state of the grid.
        """
        return {
            'width': self.width,
            'height': self.height,
            'torus': self.torus,
            # 'spaces': {f'{space.x}-{space.y}': space.state for space in self.spaces()} # This takes up too much space
        }
