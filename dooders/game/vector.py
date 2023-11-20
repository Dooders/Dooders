import math


class Vector2:
    """
    This class is a fundamental building block for many 2D games and simulations.

    It allows for easy representation and manipulation of points and directions
    in 2D space

    Attributes
    ----------
    x : int
        x component of the vector
    y : int
        y component of the vector
    thresh : float
        Threshold used for floating-point comparisons

    Methods
    -------
    __add__(other)
        Adds two vectors.
    __sub__(other)
        Subtracts two vectors.
    __neg__()
        Negates the vector.
    __mul__(scalar)
        Multiplies the vector by a scalar.
    __div__(scalar)
        Divides the vector by a scalar.
    __truediv__(scalar)
        Divides the vector by a scalar.
    __eq__(other)
        Checks if two vectors are approximately equal by comparing their x and
        y components within a threshold.
    magnitude_squared()
        Returns the squared magnitude of the vector.
    magnitude()
        Returns the magnitude of the vector.
    copy()
        Returns a copy of the vector.
    as_tuple()
        Returns the vector as a tuple.
    as_int()
        Returns the vector's components as integers. Useful for pixel-based
        operations in graphics.
    __str__()
        Provides a string representation of the vector in the format <x, y>.
    """

    def __init__(self, x: int = 0, y: int = 0) -> None:
        """
        Initializes the vector's x and y components.

        Sets a threshold (thresh) used for floating-point comparisons.

        Parameters
        ----------
        x : int
            x component of the vector
        y : int
            y component of the vector
        """
        self.x = x
        self.y = y
        self.thresh = 0.000001

    def __add__(self, other: "Vector2") -> "Vector2":
        """
        Adds two vectors.

        Parameters
        ----------
        other : Vector2
            Vector to add to this vector

        Returns
        -------
        Vector2
            Result of adding the two vectors
        """
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2") -> "Vector2":
        """
        Subtracts two vectors.

        Parameters
        ----------
        other : Vector2
            Vector to subtract from this vector

        Returns
        -------
        Vector2
            Result of subtracting the two vectors
        """
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self) -> "Vector2":
        """
        Negates the vector.

        Returns
        -------
        Vector2
            Negated vector
        """
        return Vector2(-self.x, -self.y)

    def __mul__(self, scalar: int) -> "Vector2":
        """
        Multiplies the vector by a scalar.

        Parameters
        ----------
        scalar : int
            Scalar to multiply the vector by

        Returns
        -------
        Vector2
            Result of multiplying the vector by the scalar
        """
        return Vector2(self.x * scalar, self.y * scalar)

    def __div__(self, scalar: int) -> "Vector2":
        """
        Divides the vector by a scalar.

        Parameters
        ----------
        scalar : int
            Scalar to divide the vector by

        Returns
        -------
        Vector2
            Result of dividing the vector by the scalar
        """
        if scalar != 0:
            return Vector2(self.x / float(scalar), self.y / float(scalar))
        return None

    def __truediv__(self, scalar: int) -> "Vector2":
        """
        Divides the vector by a scalar.

        Parameters
        ----------
        scalar : int
            Scalar to divide the vector by

        Returns
        -------
        Vector2
            Result of dividing the vector by the scalar
        """
        return self.__div__(scalar)

    def __eq__(self, other: "Vector2") -> bool:
        """
        Checks if two vectors are approximately equal by comparing their x and
        y components within a threshold.

        Parameters
        ----------
        other : Vector2
            Vector to compare to this vector

        Returns
        -------
        bool
            Whether the two vectors are approximately equal or not
        """
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) < self.thresh:
                return True
        return False

    def magnitude_squared(self) -> int:
        """
        Returns the squared magnitude of the vector.

        Returns
        -------
        int
            Squared magnitude of the vector
        """
        return self.x**2 + self.y**2

    def magnitude(self) -> float:
        """
        Returns the magnitude of the vector.

        Returns
        -------
        float
            Magnitude of the vector
        """
        return math.sqrt(self.magnitude_squared())

    def copy(self) -> "Vector2":
        """
        Returns a copy of the vector.

        Returns
        -------
        Vector2
            Copy of the vector
        """
        return Vector2(self.x, self.y)

    def as_tuple(self) -> tuple:
        """
        Returns the vector as a tuple.

        Returns
        -------
        tuple
            Vector as a tuple
        """
        return self.x, self.y

    def as_int(self) -> tuple:
        """
        Returns the vector's components as integers. Useful for pixel-based
        operations in graphics.

        Returns
        -------
        tuple
            Vector's components as integers
        """
        return int(self.x), int(self.y)

    def __str__(self) -> str:
        """
        Provides a string representation of the vector in the format <x, y>.

        Returns
        -------
        str
            String representation of the vector
        """
        return "<" + str(self.x) + ", " + str(self.y) + ">"