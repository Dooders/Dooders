import math

from dooders.defaults import TILE_HEIGHT, TILE_WIDTH


class Coordinate:
    """
    A coordinate is a point in 2D space. It has an x and y component, and can be
    added, subtracted, negated, multiplied, and divided by scalars. It can also
    be compared to other coordinates to check if they are approximately equal.

    Methods
    -------
    __init__(x: int = 0, y: int = 0) -> None
        Initializes the coordinate with the given x and y components
    __add__(other: Coordinate) -> Coordinate
        Adds two coordinates
    __sub__(other: Coordinate) -> Coordinate
        Subtracts two coordinates
    __neg__() -> Coordinate
        Negates the coordinate
    __mul__(scalar: int) -> Coordinate
        Multiplies the coordinate by a scalar
    __div__(scalar: int) -> Coordinate
        Divides the coordinate by a scalar
    __truediv__(scalar: int) -> Coordinate
        Divides the coordinate by a scalar
    __eq__(other: Coordinate) -> bool
        Checks if two coordinates are approximately equal by comparing their x and
        y components within a threshold
    magnitude_squared() -> int
        Returns the squared magnitude of the coordinate
    magnitude() -> float
        Returns the magnitude of the coordinate
    copy() -> Coordinate
        Returns a copy of the coordinate
    as_tuple() -> tuple
        Returns the coordinate as a tuple
    as_int() -> tuple
        Returns the coordinate's components as integers. Useful for pixel-based
        operations in graphics
    as_pixel() -> tuple
        Returns the coordinate's components as integers. Useful for pixel-based
        operations in graphics
    relative_direction(other: Coordinate) -> int
        Returns the relative direction of the other coordinate from this coordinate.
        The relative direction is an integer from 0 to 7, where 0 is directly above,
        1 is up and to the right, 2 is directly to the right, 6 is directly to the
        left, etc.
    __str__() -> str
        Provides a string representation of the coordinate in the format <x, y>
    __iter__() -> iter
        Returns an iterator for the coordinate. For example, this allows the
        coordinate to be unpacked into two variables using x, y = coordinate
    """

    EPSILON = 1e-9  # Threshold for approximate equality

    def __init__(self, x: int = 0, y: int = 0) -> None:
        """
        Parameters
        ----------
        x : int
            x component of the coordinate
        y : int
            y component of the coordinate
        """
        self.x = x
        self.y = y

    def __add__(self, other: "Coordinate") -> "Coordinate":
        """
        Adds two coordinates.

        Parameters
        ----------
        other : Coordinate
            coordinate to add to this coordinate

        Returns
        -------
        Coordinate
            Result of adding the two coordinates
        """
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Coordinate") -> "Coordinate":
        """
        Subtracts two coordinates.

        Parameters
        ----------
        other : Coordinate
            coordinate to subtract from this coordinate

        Returns
        -------
        Coordinate
            Result of subtracting the two coordinates
        """
        return Coordinate(self.x - other.x, self.y - other.y)

    def __neg__(self) -> "Coordinate":
        """
        Negates the coordinate.

        Returns
        -------
        Coordinate
            Negated coordinate
        """
        return Coordinate(-self.x, -self.y)

    def __mul__(self, scalar: int) -> "Coordinate":
        """
        Multiplies the coordinate by a scalar.

        Parameters
        ----------
        scalar : int
            Scalar to multiply the coordinate by

        Returns
        -------
        Coordinate
            Result of multiplying the coordinate by the scalar
        """
        return Coordinate(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: int) -> "Coordinate":
        """
        Divides the coordinate by a scalar.

        Parameters
        ----------
        scalar : int
            Scalar to divide the coordinate by

        Returns
        -------
        Coordinate
            Result of dividing the coordinate by the scalar
        """
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return Coordinate(self.x / scalar, self.y / scalar)

    def __eq__(self, other: "Coordinate") -> bool:
        """
        Checks if two coordinates are approximately equal by comparing their x and
        y components within a threshold.

        Parameters
        ----------
        other : Coordinate
            coordinate to compare to this coordinate

        Returns
        -------
        bool
            Whether the two coordinates are approximately equal or not
        """
        if type(other) == tuple:
            return (
                math.sqrt((self.x - other[0]) ** 2 + (self.y - other[1]) ** 2)
                < Coordinate.EPSILON
            )
        return (
            math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
            < Coordinate.EPSILON
        )

    def magnitude_squared(self) -> int:
        """
        Returns the squared magnitude of the coordinate.

        Returns
        -------
        int
            Squared magnitude of the coordinate
        """
        return self.x**2 + self.y**2

    def magnitude(self) -> float:
        """
        Returns the magnitude of the coordinate.

        Returns
        -------
        float
            Magnitude of the coordinate
        """
        return math.sqrt(self.x**2 + self.y**2)

    def copy(self) -> "Coordinate":
        """
        Returns a copy of the coordinate.

        Returns
        -------
        Coordinate
            Copy of the coordinate
        """
        return Coordinate(self.x, self.y)

    def as_tuple(self) -> tuple:
        """
        Returns the coordinate as a tuple.

        Returns
        -------
        tuple
            coordinate as a tuple
        """
        return self.x, self.y

    def as_int(self) -> tuple:
        """
        Returns the coordinate's components as integers. Useful for pixel-based
        operations in graphics.

        Returns
        -------
        tuple
            coordinate's components as integers
        """
        return int(self.x), int(self.y)

    def as_pixel(self) -> tuple:
        """
        Returns the coordinate's components as integers. Useful for pixel-based
        operations in graphics.

        Returns
        -------
        tuple
            coordinate's components as integers
        """
        return int(self.x * TILE_WIDTH), int(self.y * TILE_HEIGHT)

    def relative_direction(self, other: "Coordinate") -> int:
        """
        Returns the relative direction of the other coordinate from this coordinate.
        UP = 1
        DOWN = -1
        LEFT = 2
        RIGHT = -2

        Parameters
        ----------
        other : Coordinate
            coordinate to get the relative direction of

        Returns
        -------
        int
            Relative direction of the other coordinate from this coordinate
        """
        #! Clean this up to be simpler
        if self.x == other.x:
            if self.y < other.y:
                return -1
            else:
                return 1
        elif self.y == other.y:
            if self.x < other.x:
                return -2
            else:
                return 2
        else:
            raise ValueError("Coordinates must be adjacent to get relative direction")

    def __str__(self) -> str:
        """
        Provides a string representation of the coordinate in the format <x, y>.

        Returns
        -------
        str
            String representation of the coordinate
        """
        return str(f"[{self.x}, {self.y}]")

    def __repr__(self) -> str:
        """
        Provides a string representation of the coordinate in the format <x, y>.

        Returns
        -------
        str
            String representation of the coordinate
        """
        return str(f"[{self.x}, {self.y}]")

    def __iter__(self) -> iter:
        """
        Returns an iterator for the coordinate.

        Returns
        -------
        iter
            Iterator for the coordinate
        """
        return iter((self.x, self.y))

    def __hash__(self):
        return hash((self.x, self.y))
