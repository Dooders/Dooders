"""
Enviromenment base class.
=================
Heavily based on the space component in the Mesa library
https://github.com/projectmesa/mesa/blob/main/mesa/space.py
"""

import itertools
from abc import ABC, abstractmethod
from numbers import Real
from typing import (Any, Callable, Dict, Iterable, Iterator, List, Sequence,
                    Set, Tuple, TypeVar, Union, cast, overload)

import numpy as np
from sdk.base.base_object import BaseObject
from sdk.modules.neighborhood import Neighborhood
from sdk.modules.location import Location

Coordinate = Tuple[int, int]
Position = Coordinate
GridContent = Union[BaseObject, None]
MultiGridContent = List[GridContent]
F = TypeVar("F", bound=Callable[..., Any])


def accept_tuple_argument(wrapped_function: F) -> F:
    """Decorator to allow grid methods that take a list of (x, y) coord tuples
    to also handle a single position, by automatically wrapping tuple in
    single-item list rather than forcing user to do it."""

    def wrapper(*args: Any) -> Any:
        if isinstance(args[1], tuple) and len(args[1]) == 2:
            return wrapped_function(args[0], [args[1]])
        else:
            return wrapped_function(*args)

    return cast(F, wrapper)


def is_integer(x: Real) -> bool:
    # Check if x is either a CPython integer or Numpy integer.
    return isinstance(x, (int, np.integer))


class BaseEnvironment(ABC):
    """Base class for a square grid.
    Grid cells are indexed by [x][y], where [0][0] is assumed to be the
    bottom-left and [width-1][height-1] is the top-right. If a grid is
    toroidal, the top and bottom, and left and right, edges wrap to each other
    Properties:
        width, height: The grid's width and height.
        torus: Boolean which determines whether to treat the grid as a torus.
        grid: Internal list-of-lists which holds the grid cells themselves.
    """

    grid: List[List[MultiGridContent]]

    def __init__(self, params) -> None:
        """Create a new grid.
        Args:
            width, height: The width and height of the grid
            torus: Boolean whether the grid wraps or not.
        """
        self.height = params.Height
        self.width = params.Width
        self.torus = params.Torus

        self.grid = []

        for x in range(self.width):
            col = []
            for y in range(self.height):
                location = Location(x, y)
                col.append(location)
            self.grid.append(col)

        # Add all cells to the empties list.
        self.empties = set(itertools.product(
            *(range(self.width), range(self.height))))

        # Neighborhood Cache
        self._neighborhood_cache: Dict[Any, List[Coordinate]] = dict()

    @staticmethod
    def default_val() -> None:
        """Default value for new cell elements."""
        return None

    @overload
    def __getitem__(self, index: int) -> List[GridContent]:
        ...

    @overload
    def __getitem__(
        self, index: Tuple[int, slice]
    ) -> Union[GridContent, List[GridContent]]:
        ...

    @overload
    def __getitem__(self, index: Sequence[Coordinate]) -> List[GridContent]:
        ...

    def __getitem__(
        self,
        index: Union[int, Sequence[Coordinate], Tuple[int, slice, int, slice]],
    ) -> Union[GridContent, List[GridContent]]:
        """Access contents from the grid."""

        if isinstance(index, int):
            # grid[x]
            return self.grid[index]
        elif isinstance(index[0], tuple):
            # grid[(x1, y1), (x2, y2)]
            index = cast(Sequence[Coordinate], index)

            cells = []
            for pos in index:
                x1, y1 = self.torus_adj(pos)
                cells.append(self.grid[x1][y1])
            return cells

        x, y = index

        if is_integer(x) and is_integer(y):
            # grid[x, y]
            index = cast(Coordinate, index)
            x, y = self.torus_adj(index)
            return self.grid[x][y]

        if is_integer(x):
            # grid[x, :]
            x, _ = self.torus_adj((x, 0))
            x = slice(x, x + 1)

        if is_integer(y):
            # grid[:, y]
            _, y = self.torus_adj((0, y))
            y = slice(y, y + 1)

        # grid[:, :]
        x, y = (cast(slice, x), cast(slice, y))
        cells = []
        for rows in self.grid[x]:
            for cell in rows[y]:
                cells.append(cell)
        return cells

        raise IndexError

    def __iter__(self) -> Iterator[GridContent]:
        """Create an iterator that chains the rows of the grid together
        as if it is one list:"""
        return itertools.chain(*self.grid)

    def coord_iter(self) -> Iterator[Tuple[GridContent, int, int]]:
        """An iterator that returns coordinates as well as cell contents."""
        for row in range(self.width):
            for col in range(self.height):
                yield self.grid[row][col], row, col  # agent, x, y

    def iter_neighborhood(
        self,
        position: Coordinate,
        moore: bool = True,
        include_center: bool = False,
        radius: int = 1,
    ) -> Iterator[Coordinate]:
        """Return an iterator over cell coordinates that are in the
        neighborhood of a certain point.
        Args:
            position: Coordinate tuple for the neighborhood to get.
            moore: If True, return Moore neighborhood
                        (including diagonals)
                   If False, return Von Neumann neighborhood
                        (exclude diagonals)
            include_center: If True, return the (x, y) cell as well.
                            Otherwise, return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.
        Returns:
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
        """Return a list of locations that are in the neighborhood of a
        certain point.
        Args:
            position: Coordinate tuple for the neighborhood to get.
            moore: If True, return Moore neighborhood
                        (including diagonals)
                   If False, return Von Neumann neighborhood
                        (exclude diagonals)
            include_center: If True, return the (x, y) cell as well.
                            Otherwise, return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.
        Returns:
            A list of locations representing the neighborhood. For
            example with radius 1, it will return list with number of elements
            equals at most 9 (8) if Moore, 5 (4) if Von Neumann (if not
            including the center).
        """
        neighborhood = self.get_neighborhood(position, moore, include_center, radius)
        return [self.grid[pos[0]][pos[1]] for pos in neighborhood]
    
    
    def get_neighborhood(
        self,
        position: Coordinate,
        moore: bool = True,
        include_center: bool = False,
        radius: int = 1,
    ) -> List[Coordinate]:
        """Return a list of cells that are in the neighborhood of a
        certain point.
        Args:
            position: Coordinate tuple for the neighborhood to get.
            moore: If True, return Moore neighborhood
                   (including diagonals)
                   If False, return Von Neumann neighborhood
                   (exclude diagonals)
            include_center: If True, return the (x, y) cell as well.
                            Otherwise, return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.
        Returns:
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

    def iter_neighbors(
        self,
        position: Coordinate,
        moore: bool = True,
        include_center: bool = False,
        radius: int = 1,
    ) -> Iterator[BaseObject]:
        """Return an iterator over neighbors to a certain point.
        Args:
            pos: Coordinates for the neighborhood to get.
            moore: If True, return Moore neighborhood
                    (including diagonals)
                   If False, return Von Neumann neighborhood
                     (exclude diagonals)
            include_center: If True, return the (x, y) cell as well.
                            Otherwise,
                            return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.
        Returns:
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
    ) -> List[BaseObject]:
        """Return a list of neighbors to a certain point.
        Args:
            position: Coordinate tuple for the neighborhood to get.
            moore: If True, return Moore neighborhood
                    (including diagonals)
                   If False, return Von Neumann neighborhood
                     (exclude diagonals)
            include_center: If True, return the (x, y) cell as well.
                            Otherwise,
                            return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.
        Returns:
            A list of non-None objects in the given neighborhood;
            at most 9 if Moore, 5 if Von-Neumann
            (8 and 4 if not including the center).
        """
        return list(self.iter_neighbors(position, moore, include_center, radius))

    def torus_adj(self, position: Coordinate) -> Coordinate:
        """Convert coordinate, handling torus looping."""
        if not self.out_of_bounds(position):
            return position
        elif not self.torus:
            raise Exception("Point out of bounds, and space non-toroidal.")
        else:
            return position[0] % self.width, position[1] % self.height

    def out_of_bounds(self, position: Coordinate) -> bool:
        """Determines whether position is off the grid, returns the out of
        bounds coordinate."""
        x, y = position
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    @accept_tuple_argument
    def get_cell_list_contents(self, cell_list: Iterable[Coordinate]) -> List[BaseObject]:
        """Returns a list of the contents of the cells
        identified in cell_list.
        Note: this method returns a list of `Agent`'s; `None` contents are excluded.
        Args:
            cell_list: Array-like of (x, y) tuples, or single tuple.
        Returns:
            A list of the contents of the cells identified in cell_list
        """
        return list(self.iter_cell_list_contents(cell_list))

    def is_cell_empty(self, position: Coordinate) -> bool:
        """Returns a bool of the contents of a cell."""
        x, y = position
        return self.grid[x][y].status == 'empty'

    def exists_empty_cells(self) -> bool:
        """Return True if any cells empty else False."""
        return len(self.empties) > 0

    @staticmethod
    def default_val() -> MultiGridContent:
        """Default value for new cell elements."""
        return []

    @accept_tuple_argument
    def iter_cell_list_contents(
        self, cell_list: Iterable[Coordinate]
    ) -> Iterator[MultiGridContent]:
        """Returns an iterator of the contents of the
        cells identified in cell_list.
        Args:
            cell_list: Array-like of (x, y) tuples, or single tuple.
        Returns:
            A iterator of the contents of the cells identified in cell_list
        """
        return itertools.chain.from_iterable(
            self[x][y].contents.values() for x, y in cell_list if not self.is_cell_empty((x, y))
        )
