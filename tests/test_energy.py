
import pytest

from tests.test_util import mock_simulation
from sdk.environment import Energy


@pytest.fixture
def energy():
    simulation = mock_simulation()
    object = Energy('3', (3, 3), simulation, simulation.params.Energy)
    simulation.environment.place_object(object, (3, 3))
    simulation.time.add(object)

    return object, simulation


def test_energy_init(energy):
    object, _ = energy
    assert object.unique_id == '3'
    assert object.position == (3, 3)
    assert object.life_span >= 2 and object.life_span <= object.params.MaxLifespan
    assert object.cycle_count == 0


def test_energy_step(energy):
    object, _ = energy
    object.step()
    assert object.cycle_count == 1


def test_energy_dissipation(energy):
    object, simulation = energy
    lifespan = object.life_span
    for i in range(lifespan):
        object.step()
    assert i == lifespan - 1
    assert object.cycle_count == lifespan
    assert object not in simulation.environment.get_objects(Energy)
    assert object not in simulation.time.get_objects(Energy)


def test_energy_consumption(energy):
    object, simulation = energy
    object.consume()
    assert object not in simulation.environment.get_objects(Energy)
    assert object not in simulation.time.get_objects(Energy)
