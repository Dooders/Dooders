# import pytest
# from sdk.core import Strategy

# from tests.test_util import mock_simulation
# from sdk.models import Energy
# from sdk.models.resources import Resources

# EnergyStrategy = Strategy.load_strategy('energy')

# @pytest.fixture
# def energy():
#     simulation = mock_simulation()
#     object = Energy('3', (3, 3), simulation.resources)
#     simulation.environment.place_object(object, (3, 3))

#     return object, simulation


# def test_energy_init(energy):
#     object, _ = energy
#     assert object.id == '3'
#     assert object.position == (3, 3)
#     assert object.cycle_count == 0


# def test_energy_step(energy):
#     object, _ = energy
#     object.step()
#     assert object.cycle_count == 1
