import math
from typing import Any

from dooders.games.pacman.settings import Directions


class Vector2D:
    """
    A 2D vector class

    Attributes
    ----------
    x : float
        x component of the vector
    y : float
        y component of the vector

    Properties
    ----------
    magnitude : float
        Magnitude of the vector
    angle : float
        Angle of the vector in radians

    Methods
    -------
    __add__(other: Vector2D) -> Vector2D
        Add two vectors
    __sub__(other: Vector2D) -> Vector2D
        Subtract two vectors
    __mul__(scalar: float) -> Vector2D
        Multiply the vector by a scalar
    __truediv__(scalar: float) -> Vector2D
        Divide the vector by a scalar
    dot(other: Vector2D) -> float
        Calculate the dot product of two vectors
    normalize() -> Vector2D
        Normalize the vector by dividing it by its magnitude
    distance(v1: Vector2D, v2: Vector2D) -> float
        Calculate the distance between two vectors
    angle_between(v1: Vector2D, v2: Vector2D) -> float
        Calculate the angle between two vectors
    copy() -> Vector2D
        Returns a copy of the vector
    """

    def __init__(self, x: float, y: float) -> None:
        """
        Initialize the vector with x and y components

        Parameters
        ----------
        x : float
            x component of the vector
        y : float
            y component of the vector
        """
        self._x = x
        self._y = y
        self._magnitude = None
        self._angle = None

    @property
    def x(self) -> float:
        """
        x component of the vector

        Returns
        -------
        float
            x component of the vector
        """
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """
        Set the x component of the vector

        Parameters
        ----------
        value : float
            The new x component of the vector
        """
        self._x = value
        self._magnitude = None
        self._angle = None

    @property
    def y(self) -> float:
        """
        y component of the vector

        Returns
        -------
        float
            y component of the vector
        """
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        """
        Set the y component of the vector

        Parameters
        ----------
        value : float
            The new y component of the vector
        """
        self._y = value
        self._magnitude = None
        self._angle = None

    @property
    def magnitude(self) -> float:
        """
        Magnitude of the vector

        Returns
        -------
        float
            Magnitude of the vector
        """
        return math.sqrt(self.x**2 + self.y**2)

    @property
    def magnitude_squared(self) -> float:
        """
        Magnitude of the vector squared

        Returns
        -------
        float
            Squared magnitude of the vector
        """
        return self.x**2 + self.y**2

    @property
    def angle(self) -> float:
        """
        Angle of the vector

        Returns
        -------
        float
            Angle of the vector in radians
        """
        return math.atan2(self.y, self.x)

    def copy(self) -> "Vector2D":
        """
        Returns a copy of the vector.

        Returns
        -------
        Vector2D
            Copy of the vector
        """
        return self.__class__(self.x, self.y)

    def __add__(self, other: "Vector2D") -> "Vector2D":
        """
        Add two vectors

        Parameters
        ----------
        other : Vector2D
            The vector to be added

        Returns
        -------
        Vector2D
            The sum of the two vectors
        """
        if not isinstance(other, Vector2D):
            raise TypeError("Operand must be a Vector2D")
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        """
        Subtract two vectors

        Parameters
        ----------
        other : Vector2D
            The vector to be subtracted

        Returns
        -------
        Vector2D
            The difference of the two vectors
        """
        if not isinstance(other, Vector2D):
            raise TypeError("Operand must be a Vector2D")
        return self.__class__(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector2D":
        """
        Multiply the vector by a scalar

        Parameters
        ----------
        scalar : float
            The scalar to multiply the vector by

        Returns
        -------
        Vector2D
            The product of the vector and the scalar
        """
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> "Vector2D":
        """
        Divide the vector by a scalar

        Parameters
        ----------
        scalar : float
            The scalar to divide the vector by

        Returns
        -------
        Vector2D
            The quotient of the vector and the scalar
        """
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector2D(self.x / scalar, self.y / scalar)

    def __eq__(self, other: "Vector2D") -> bool:
        """
        Check if two vectors are equal

        Parameters
        ----------
        other : Any
            The object to compare to

        Returns
        -------
        bool
            True if the vectors are equal, False otherwise
        """
        if not isinstance(other, Vector2D):
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: "Vector2D") -> bool:
        """
        Check if two vectors are not equal

        Parameters
        ----------
        other : Any
            The object to compare to

        Returns
        -------
        bool
            True if the vectors are not equal, False otherwise
        """
        return not self.__eq__(other)

    def __neg__(self) -> "Vector2D":
        """
        Negate the vector

        Returns
        -------
        Vector2D
            Negated vector
        """
        return Vector2D(-self.x, -self.y)

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

    def dot(self, other: "Vector2D") -> float:
        """
        Calculate the dot product of two vectors

        Parameters
        ----------
        other : Vector2D
            The vector to calculate the dot product with

        Returns
        -------
        float
            The dot product of the two vectors
        """
        return self.x * other.x + self.y * other.y

    def normalize(self) -> "Vector2D":
        """
        Normalize the vector by dividing it by its magnitude

        Returns
        -------
        Vector2D
            The normalized vector
        """
        magnitude = self.magnitude
        if magnitude == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / magnitude, self.y / magnitude)

    def distance_to(self, other: "Vector2D") -> float:
        """
        Returns the manhattan distance between two coordinates.

        Parameters
        ----------
        other : Coordinate
            coordinate to get the distance to

        Returns
        -------
        float
            Manhattan distance between the two coordinates
        """
        return abs(self.x - other.x) + abs(self.y - other.y)

    def direction_to(self, other: "Vector2D") -> "Vector2D":
        """
        Returns the direction to another vector.

        Parameters
        ----------
        other : Vector2D
            The vector to get the direction to

        Returns
        -------
        Vector2D
            The direction to the other vector
        """
        if self.x == other.x:
            if self.y < other.y:
                return Directions.DOWN
            else:
                return Directions.UP
        elif self.y == other.y:
            if self.x < other.x:
                return Directions.RIGHT
            else:
                return Directions.LEFT
        else:
            raise ValueError("Vectors must be adjacent to get relative direction")

    @staticmethod
    def angle_between(v1: "Vector2D", v2: "Vector2D") -> float:
        """
        Calculate the angle between two vectors

        Parameters
        ----------
        v1 : Vector2D
            The first vector
        v2 : Vector2D
            The second vector

        Returns
        -------
        float
            The angle between the two vectors
        """
        dot_product = v1.dot(v2)
        magnitudes = v1.magnitude * v2.magnitude
        if magnitudes == 0:
            return 0
        angle = math.acos(dot_product / magnitudes)
        return angle

    def as_tuple(self) -> tuple:
        """
        Return the vector as a tuple

        Returns
        -------
        tuple
            The vector as a tuple
        """
        return self.x, self.y

    def as_int_tuple(self) -> tuple:
        """
        Return the vector as a tuple of integers

        Returns
        -------
        tuple
            The vector as a tuple of integers
        """
        return int(self.x), int(self.y)


class Acceleration(Vector2D):
    """A 2D acceleration vector"""

    pass


class Velocity(Vector2D):
    """A 2D velocity vector"""

    pass


class Force(Vector2D):
    """A 2D force vector"""

    pass


class Coordinate(Vector2D):
    """A 2D coordinate vector"""

    pass
