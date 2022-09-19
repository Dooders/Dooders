import pytest

from sdk.dooder.society import Society
from tests.test_util import mock_simulation


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