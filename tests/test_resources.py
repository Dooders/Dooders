# import pytest
# from sdk.models.resources import Resources

# from tests.test_util import mock_simulation


# @pytest.fixture
# def simulation():
#     simulation = mock_simulation()

#     return simulation


# def test_init():
#     simulation = mock_simulation()
#     resources = Resources(simulation)
#     assert resources.available_resources == {}
#     assert resources.allocated_energy == 0


# def test_allocate_resources(simulation):
#     simulation.resources.allocate_resources()
#     assert simulation.resources.available_resources != {}
#     assert simulation.resources.allocated_energy > 0


# def test_step(simulation):
#     available_resources = simulation.resources.available_resources
#     simulation.resources.step()
#     updated_resources = simulation.resources.available_resources
#     assert len(available_resources) >= len(updated_resources)


# def test_remove(simulation):
#     simulation.resources.step()
#     energy = list(simulation.resources.available_resources.values())[0]
#     simulation.resources.remove(energy)
#     assert energy.id not in simulation.resources.available_resources
