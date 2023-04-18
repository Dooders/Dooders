import pytest

from sdk.simulation import Simulation
from tests.test_util import test_config



@pytest.fixture
def simulation():
    return Simulation('testing', 'testing', test_config)


@pytest.fixture
def setup_simulation(simulation):
    simulation.setup()
    return simulation


def test_simulation_initialization(simulation):
    assert simulation.cycle_number == 0



def test_simulation_setup(simulation):
    simulation.setup()
    assert simulation.running == True


def test_run_simulation(simulation):
    simulation.run_simulation()


# def test_reset(setup_simulation):
#     simulation = setup_simulation
#     simulation.reset()
#     assert simulation.steps == 0
#     assert simulation.running == True
#     # assert len(simulation.time._objects) == 30
#     assert len(simulation.environment.get_objects()) == 30
#     assert len(simulation.environment.get_objects(Dooder)) == 10
#     assert len(simulation.environment.get_objects(Energy)) == 20


def test_stop(setup_simulation):
    simulation = setup_simulation
    simulation.stop()
    assert simulation.running == False


def test_cycle(setup_simulation):
    simulation = setup_simulation
    simulation.cycle()
    assert simulation.cycle_number == 1
    assert simulation.running == True


