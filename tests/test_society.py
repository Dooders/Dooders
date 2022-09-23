import pytest

from sdk.dooder.society import Society
from sdk.mocks import mock_simulation


@pytest.fixture
def society():
    simulation = mock_simulation()
    society = Society(simulation)
    
    return society, simulation


def test_init():
    simulation = mock_simulation()
    assert Society(simulation)


def test_generate_seed_population(society):
    society, _ = society
    society.generate_seed_population()
    assert society.active_dooders != {}
    assert society.total_created_dooders > 0
    
    
def test_generate_dooder(society):
    society, _ = society
    society.generate_dooder((1,1))
    assert society.active_dooders != {}
    assert society.total_created_dooders > 0


def test_place_dooder(society):
    society, simulation = society
    society.generate_dooder((1,1))
    assert simulation.environment.grid[1][1] != None
    
    
def test_properties():
    simulation = mock_simulation()
    society = Society(simulation)
    assert society.active_dooders == {}
    assert society.total_created_dooders == 0
    assert society.graveyard == {}
    assert society.graph != None
    
#! need to make this work
# def test_terminate_dooder(society):
#     society, simulation = society
#     society.generate_dooder((1,1))
#     dooder = simulation.environment.get_dooder((1,1))
#     society.terminate_dooder(dooder)
#     assert simulation.environment.grid[1][1] == None