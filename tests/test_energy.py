import pytest
from sdk.strategies.strategies import Strategies

from tests.test_util import mock_simulation
from sdk.environment import Energy
from sdk.environment.resources import Resources

EnergyStrategy = Strategies.load_strategy('sdk/environment/energy.yml')

@pytest.fixture
def energy():
    simulation = mock_simulation()
    object = Energy('3', (3, 3), Resources)
    simulation.environment.place_object(object, (3, 3))

    return object, simulation


def test_energy_init(energy):
    object, _ = energy
    assert object.unique_id == '3'
    assert object.position == (3, 3)
    assert object.cycle_count == 0


def test_energy_step(energy):
    object, _ = energy
    object.step()
    assert object.cycle_count == 1


def test_energy_dissipation(energy):
    object, simulation = energy
    lifespan = object.Lifespan
    for i in range(lifespan):
        object.step()
    assert i == lifespan - 1
    assert object.cycle_count == lifespan
    assert object not in simulation.environment.get_objects(Energy)


def test_energy_consumption(energy):
    object, simulation = energy
    object.consume()
    assert object not in simulation.environment.get_objects(Energy)
