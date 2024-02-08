import unittest

from dooders.sdk.base.entity import Entity
from dooders.sdk.utils.short_id import seed


class MockEntity(Entity):
    def update(self):
        self.age += 1  # Simple implementation for testing


class TestEntity(unittest.TestCase):
    def setUp(self):
        self.mock_settings = {"position": (5, 5), "created": 100}
        self.entity = MockEntity(settings=self.mock_settings)

    def test_initialization(self):
        """Test that the entity is initialized with the correct settings."""
        self.assertEqual(self.entity.position, (5, 5))
        self.assertEqual(self.entity.created, 100)
        self.assertIsNone(self.entity.terminated)
        self.assertEqual(self.entity.age, 0)
        self.assertEqual(len(self.entity._history), 0)

    def test_name_property(self):
        """Test the name property."""
        self.assertEqual(self.entity.name, "MockEntity")

    def test_partial_state_property(self):
        """Test the partial_state property."""
        expected_partial_state = {
            "id": self.entity.id,  # ID is generated dynamically
            "created": 100,
            "terminated": None,
            "age": 0,
            "position": (5, 5),
        }
        self.assertEqual(self.entity.partial_state, expected_partial_state)

    def test_state_property(self):
        """Test the state property, including history."""
        self.entity._history.append("test_event")  # Simulate an event
        expected_state = {
            "id": self.entity.id,  # ID is generated dynamically
            "created": 100,
            "terminated": None,
            "age": 0,
            "position": (5, 5),
            "history": ["test_event"],
        }
        self.assertEqual(self.entity.state, expected_state)

    def test_update_method(self):
        """Test that the update method correctly modifies the entity's state."""
        self.entity.update()
        self.assertEqual(self.entity.age, 1)


if __name__ == "__main__":
    unittest.main()
