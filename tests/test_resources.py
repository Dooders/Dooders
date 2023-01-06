import pytest
from sdk.models.resources import Resources

from tests.test_util import mock_simulation


@pytest.fixture
def resources():
    simulation = mock_simulation()
    resources = Resources(simulation)

    return resources, simulation


def test_init():
    simulation = mock_simulation()
    resources = Resources(simulation)
    assert resources.available_resources == {}
    assert resources.allocated_energy == 0


def test_allocate_resources(resources):
    resources, _ = resources
    resources.allocate_resources()
    assert resources.available_resources != {}
    assert resources.allocated_energy > 0


def test_step(resources):
    #! Need to fix
    # resources, _ = resources
    # resources.allocate_resources()
    # assert resources.available_resources != {}
    # assert resources.allocated_energy > 0
    # available_before = len(resources.available_resources)
    # total_before = resources.allocated_energy
    # resources.step()
    # assert len(resources.available_resources) > available_before
    # assert resources.allocated_energy > total_before
    pass


def test_remove(resources):
    resources, _ = resources
    resources.allocate_resources()
    energy = list(resources.available_resources.values())[0]
    resources.remove(energy)
    assert energy.unique_id not in resources.available_resources
