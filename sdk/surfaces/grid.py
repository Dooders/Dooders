import itertools
from functools import singledispatchmethod
from numbers import Real
from typing import Any, Iterable, Iterator, List, Sequence, Tuple, cast

import numpy as np

from sdk.modules.location import Location

GridRow = List[Location]
Coordinate = Tuple[int, int]

#! this will inherit surface???

def accept_tuple_argument(wrapped_function) -> Any:
    """
    Decorator to allow surface methods that take a list of (x, y) coord tuples
    to also handle a single position, by automatically wrapping tuple in
    single-item list rather than forcing user to do it.
    """

    def wrapper(*args: Any) -> Any:
        if isinstance(args[1], tuple) and len(args[1]) == 2:
            return wrapped_function(args[0], [args[1]])
        else:
            return wrapped_function(*args)

    return wrapper

def is_integer(x: Real) -> bool:
    # Check if x is either a CPython integer or Numpy integer.
    return isinstance(x, (int, np.integer))

class Grid:
    """
    """

    _empties: List[Coordinate]
    _grid: List[List[GridRow]]

    def __init__(self, settings) -> None:

        self._grid = []

        self.width = settings['width']
        self.height = settings['height']

        for x in range(settings['width']):
            col = []
            for y in range(settings['height']):
                location = Location(x, y)
                col.append(location)
            self._grid.append(col)

        # Creates all coordinates in a set, in order
        self._empties = set(itertools.product(
            *(range(settings['width']), range(settings['height']))))

        # Neighborhood Cache
        self._neighborhood_cache = {}

    @singledispatchmethod
    def __getitem__(self, value):
        raise NotImplementedError(f'Type {type(value)} is unsupported')

    @__getitem__.register
    def _(self, value: int):
        return self._grid[value]

    @__getitem__.register
    def _(self, value: list):
        index = cast(Sequence[Coordinate], value)

        cells = []
        for pos in index:
            x1, y1 = self.torus_adj(pos)
            cells.append(self._grid[x1][y1])
        return cells

    @__getitem__.register
    def _(self, value: tuple):
        index = cast(Coordinate, value)
        x, y = self.torus_adj(index)
        return self._grid[x][y]

    def __iter__(self) -> Iterator[GridRow]:
        """
        Create an iterator that chains the rows of the surface together
        as if it is one list.

        Returns
        -------
        Iterator[GridContent]
            The iterator of the surface.
        """
        return itertools.chain(*self._grid)

    def coord_iter(self) -> Iterator[Tuple[Location, int, int]]:
        """
        An iterator that returns Location and its coordinates.

        Returns
        -------
        Iterator[Tuple[GridContent, int, int]]
            The iterator of the surface.
        """
        for row in range(self.width):
            for col in range(self.height):
                yield self._grid[row][col], row, col

    def get_neighborhood(
        self,
        position: Coordinate,
        moore: bool = True,
        include_center: bool = False,
        radius: int = 1,
    ) -> List[Coordinate]:
        """
        Return a list of cells that are in the neighborhood of a
        certain point.

        Parameters
        ----------
        position: Coordinate
            Coordinate tuple for the neighborhood to get.
        moore: bool
            If True, return Moore neighborhood (including diagonals)
            If False, return Von Neumann neighborhood (exclude diagonals)
        include_center: bool
            If True, return the (x, y) cell as well.
            Otherwise, return surrounding cells only.
        radius: int
            radius, in cells, of neighborhood to get.

        Returns
        -------
            A list of coordinate tuples representing the neighborhood;
            With radius 1, at most 9 if Moore, 5 if Von Neumann (8 and 4
            if not including the center).
        """
        cache_key = (position, moore, include_center, radius)
        neighborhood = self._neighborhood_cache.get(cache_key, None)

        if neighborhood is None:
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
                        coord = self.torus_adj(coord)

                    coordinates.append(coord)

            neighborhood = coordinates
            self._neighborhood_cache[cache_key] = neighborhood

        return neighborhood

    def iter_neighborhood(
        self,
        position: Coordinate,
        moore: bool = True,
        include_center: bool = False,
        radius: int = 1,
    ) -> Iterator[Coordinate]:
        """
        Return an iterator over cell coordinates that are in the
        neighborhood of a certain point.

        Parameters
        ----------
        position: Coordinate
            Coordinate tuple for the neighborhood to get.
        moore: bool
            If True, return Moore neighborhood (including diagonals)
            If False, return Von Neumann neighborhood(exclude diagonals)
        include_center: bool
            If True, return the (x, y) cell as well.
            Otherwise, return surrounding cells only.
        radius: int
            radius, in cells, of neighborhood to get.

        Returns
        -------
            A list of coordinate tuples representing the neighborhood. For
            example with radius 1, it will return list with number of elements
            equals at most 9 (8) if Moore, 5 (4) if Von Neumann (if not
            including the center).
        """
        yield from self.get_neighborhood(position, moore, include_center, radius)

    def get_neighbor_locations(
        self,
        position: Coordinate,
        moore: bool = True,
        include_center: bool = True,
        radius: int = 1,
    ) -> List[Location]:
        """
        Return a list of locations that are in the neighborhood of a
        certain point.

        Parameters
        ----------
        position: Coordinate
            Coordinate tuple for the neighborhood to get.
        moore: bool
            If True, return Moore neighborhood (including diagonals)
            If False, return Von Neumann neighborhood(exclude diagonals)
        include_center: bool
            If True, return the (x, y) cell as well.
            Otherwise, return surrounding cells only.
        radius: int
            radius, in cells, of neighborhood to get.

        Returns
        -------
            A list of locations representing the neighborhood. For
            example with radius 1, it will return list with number of elements
            equals at most 9 (8) if Moore, 5 (4) if Von Neumann (if not
            including the center).
        """
        neighborhood = self.get_neighborhood(
            position, moore, include_center, radius)
        return [self.surface[pos[0]][pos[1]] for pos in neighborhood]

    def iter_neighbors(
        self,
        position: Coordinate,
        moore: bool = True,
        include_center: bool = False,
        radius: int = 1,
    ) -> Iterator[object]:
        """
        Return an iterator over neighbors to a certain point.

        Parameters
        ----------
        pos: Coordinate
            Coordinates for the neighborhood to get.
        moore: bool
            If True, return Moore neighborhood (including diagonals)
            If False, return Von Neumann neighborhood (exclude diagonals)
        include_center: bool
            If True, return the (x, y) cell as well.
            Otherwise, return surrounding cells only.
        radius: int
            radius, in cells, of neighborhood to get.

        Returns
        -------
            An iterator of non-None objects in the given neighborhood;
            at most 9 if Moore, 5 if Von-Neumann
            (8 and 4 if not including the center).
        """
        neighborhood = self.get_neighborhood(
            position, moore, include_center, radius)
        return self.iter_cell_list_contents(neighborhood)

    def get_neighbors(
        self,
        position: Coordinate,
        moore: bool = True,
        include_center: bool = False,
        radius: int = 1,
    ) -> List[object]:
        """
        Return a list of neighbors to a certain point.

        Parameters
        ----------
        position: Coordinate
            Coordinate tuple for the neighborhood to get.
        moore: bool
            If True, return Moore neighborhood (including diagonals)
            If False, return Von Neumann neighborhood (exclude diagonals)
        include_center: bool
            If True, return the (x, y) cell as well.
            Otherwise, return surrounding cells only.
        radius: int
            radius, in cells, of neighborhood to get.

        Returns
        -------
            A list of non-None objects in the given neighborhood;
            at most 9 if Moore, 5 if Von-Neumann
            (8 and 4 if not including the center).
        """
        return list(self.iter_neighbors(position, moore, include_center, radius))

    @accept_tuple_argument
    def iter_cell_list_contents(
        self, cell_list: Iterable[Coordinate]
    ) -> Iterator[object]:
        """
        Returns an iterator of the contents of the
        cells identified in cell_list.

        Parameters
        ----------
        cell_list: Array-like 
            of (x, y) tuples, or single tuple.

        Returns
        -------
            A iterator of the contents of the cells identified in cell_list
        """
        return itertools.chain.from_iterable(
            self[x][y].contents.values() for x, y in cell_list if not self.is_cell_empty((x, y))
        )

    @accept_tuple_argument
    def get_cell_list_contents(self, cell_list: Iterable[Coordinate]) -> List[object]:
        """
        Returns a list of the contents of the cells
        identified in cell_list.
        Note: this method returns a list of `Agent`'s; `None` contents are excluded.

        Parameters
        ----------
        cell_list: Array-like 
            of (x, y) tuples, or single tuple.

        Returns
        -------
            A list of the contents of the cells identified in cell_list
        """
        return list(self.iter_cell_list_contents(cell_list))

    def torus_adj(self, position: Coordinate) -> Coordinate:
        """
        Convert coordinate, handling torus looping.

        Parameters
        ----------
        position: Coordinate
            Coordinate tuple to convert.

        Returns
        -------
            A coordinate tuple, converted to be on the surface.
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
            True if position is off the surface, False otherwise.
        """
        x, y = position
        return x < 0 or x >= self.width or y < 0 or y >= self.height
    
    def is_cell_empty(self, position: Coordinate) -> bool:
        """
        Returns a bool of the contents of a cell.

        Parameters
        ----------
        position: Coordinate
            Coordinate tuple of the cell to check.

        Returns
        -------
            True if cell is empty, False otherwise
        """
        x, y = position
        return self.surface[x][y].status == 'empty'

    def exists_empty_cells(self) -> bool:
        """
        Return True if any cells empty else False.

        Returns
        -------
            True if any cells empty else False.
        """
        return len(self.empties) > 0
    