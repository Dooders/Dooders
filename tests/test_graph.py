import unittest
from dooders.sdk.surfaces.graph import Graph


class TestGraphMethods(unittest.TestCase):
    def setUp(self):
        # Initialize a new graph for each test
        self.graph = Graph(settings={"torus": True, "width": 10, "height": 10})
        self.test_object = object()
        self.graph.add(self.test_object, (5, 5))

    def test_update_position(self):
        # Test updating the position of an object
        self.graph.update_position(self.test_object, (6, 6))
        self.assertIn(self.test_object, self.graph.contents(6, 6))
        self.assertNotIn(self.test_object, self.graph.contents(5, 5))

    def test_add_multiple_objects(self):
        # Test adding multiple objects and checking their positions
        second_object = object()
        third_object = object()
        self.graph.add(second_object, (2, 2))
        self.graph.add(third_object, (3, 3))

        self.assertIn(second_object, self.graph.contents(2, 2))
        self.assertIn(third_object, self.graph.contents(3, 3))

    def test_remove_object(self):
        # Test removing an object
        self.graph.remove(self.test_object)
        self.assertNotIn(self.test_object, self.graph.contents(5, 5))

    def test_clear_space(self):
        # Test clearing a space of all objects
        second_object = object()
        self.graph.add(second_object, (5, 5))
        self.graph.clear_space((5, 5))

        self.assertNotIn(self.test_object, self.graph.contents(5, 5))
        self.assertNotIn(second_object, self.graph.contents(5, 5))

    def test_get_all_objects(self):
        # Test getting all objects in the graph
        objects = self.graph.get_all_objects()
        self.assertIn(self.test_object, objects)

    def test_space_occupancy(self):
        # Test checking if a space is occupied
        self.assertTrue(self.graph.is_occupied((5, 5)))
        self.assertFalse(self.graph.is_occupied((1, 1)))

    def test_coordinate_to_node_label(self):
        # Test the coordinate_to_node_label method
        self.assertEqual(self.graph.coordinate_to_node_label(0, 0), 0)
        self.assertEqual(self.graph.coordinate_to_node_label(1, 0), 1)
        self.assertEqual(self.graph.coordinate_to_node_label(0, 1), 10)

    def test_add_remove_object(self):
        # Test the add and remove object methods
        test_object = object()  # Create a generic object
        test_coordinate = (1, 1)
        self.graph.add(test_object, test_coordinate)
        self.assertIn(
            test_object, self.graph._graph.nodes[11]["space"]
        )  # Assuming 11 is the label for (1, 1)

        self.graph.remove(test_object)
        self.assertNotIn(test_object, self.graph._graph.nodes[11]["space"])

    def test_spaces(self):
        # Test the spaces method
        spaces = list(self.graph.spaces())
        self.assertEqual(len(spaces), 100)  # 10x10 grid

    def test_out_of_bounds(self):
        # Test the out_of_bounds method
        self.assertTrue(self.graph.out_of_bounds((-1, -1)))
        self.assertFalse(self.graph.out_of_bounds((5, 5)))

    def test_contents(self):
        # Test the contents method
        self.assertIn(self.test_object, self.graph.contents(5, 5))
        self.assertNotIn(self.test_object, self.graph.contents(0, 0))

    def test_nearby_spaces(self):
        # Test the nearby_spaces method
        nearby = list(self.graph.nearby_spaces((5, 5), distance=1))
        self.assertIn((5, 6), nearby)  # Check if a nearby space is correctly identified
        self.assertNotIn((0, 0), nearby)  # Check a non-nearby space

    def test_coordinate_wrap(self):
        # Test the coordinate wrapping functionality if your graph supports it
        wrapped_coordinate = self.graph.coordinate_wrap((11, 11))
        self.assertEqual(wrapped_coordinate, (1, 1))

    def test_distance(self):
        # Test the distance method if available
        distance = self.graph.distance((0, 0), (9, 9))
        self.assertEqual(distance, 2)  # Assuming torus topology

    def test_add_object_at_invalid_position(self):
        # Test adding an object at an invalid position
        with self.assertRaises(ValueError):
            self.graph.add(self.test_object, (-1, -1))

    def test_remove_nonexistent_object(self):
        # Test removing an object that isn't present
        non_existent_object = object()
        with self.assertRaises(KeyError):
            self.graph.remove(non_existent_object)


if __name__ == "__main__":
    unittest.main()
