import unittest
import math
from dooders.sdk.base.coordinate import Coordinate


class TestCoordinate(unittest.TestCase):
    def test_init(self):
        coord = Coordinate(3, 4)
        self.assertEqual(coord.x, 3)
        self.assertEqual(coord.y, 4)

    def test_add(self):
        coord1 = Coordinate(1, 2)
        coord2 = Coordinate(3, 4)
        result = coord1 + coord2
        self.assertEqual(result, Coordinate(4, 6))

    def test_sub(self):
        coord1 = Coordinate(5, 7)
        coord2 = Coordinate(2, 3)
        result = coord1 - coord2
        self.assertEqual(result, Coordinate(3, 4))

    def test_neg(self):
        coord = Coordinate(1, -2)
        result = -coord
        self.assertEqual(result, Coordinate(-1, 2))

    def test_mul(self):
        coord = Coordinate(3, -4)
        result = coord * 2
        self.assertEqual(result, Coordinate(6, -8))

    def test_truediv(self):
        coord = Coordinate(10, -20)
        result = coord / 2
        self.assertEqual(result, Coordinate(5, -10))
        with self.assertRaises(ZeroDivisionError):
            _ = coord / 0

    def test_eq(self):
        self.assertTrue(Coordinate(1.00001, 1.00002) == Coordinate(1.00002, 1.00003))
        self.assertFalse(Coordinate(1.0001, 1.0001) == Coordinate(1.0002, 1.0002))

    def test_magnitude(self):
        coord = Coordinate(3, 4)
        self.assertEqual(coord.magnitude(), 5)

    def test_as_tuple(self):
        coord = Coordinate(3, 4)
        self.assertEqual(coord.as_tuple(), (3, 4))

    def test_as_int(self):
        coord = Coordinate(3.7, 4.2)
        self.assertEqual(coord.as_int(), (3, 4))

    def test_str(self):
        coord = Coordinate(3, 4)
        self.assertEqual(str(coord), "<3, 4>")

    def test_copy(self):
        coord = Coordinate(3, 4)
        copy_coord = coord.copy()
        self.assertEqual(coord, copy_coord)
        self.assertNotEqual(
            id(coord), id(copy_coord)
        )  # Ensure they are different instances

    def test_as_pixel(self):
        TILE_WIDTH = 10
        TILE_HEIGHT = 15
        coord = Coordinate(3, 4)
        self.assertEqual(coord.as_pixel(), (30, 60))  # 3 * 10, 4 * 15

    def test_relative_direction(self):
        coord1 = Coordinate(0, 0)
        coord2 = Coordinate(1, 1)
        self.assertEqual(coord1.relative_direction(coord2), 1)

        coord2 = Coordinate(0, 1)
        self.assertEqual(coord1.relative_direction(coord2), 0)

        coord2 = Coordinate(-1, -1)
        self.assertEqual(coord1.relative_direction(coord2), 5)


if __name__ == "__main__":
    unittest.main()
