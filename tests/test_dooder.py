import pytest
from sdk.dooder import Dooder
from sdk.utils.mocks import mock_dooder, mock_simulation


@pytest.fixture
def dooder():
    simulation = mock_simulation()
    unique_id = simulation.generate_id()
    object = Dooder(unique_id, (1,1), simulation)
    simulation.environment.place_object(object, (1,1))
    simulation.time.add(object)
    
    return object, simulation


def test_dooder_init():
    simulation = mock_simulation()
    unique_id = simulation.generate_id()
    dooder = Dooder(unique_id, (1,1), simulation)
    assert dooder.position == (1,1)
    assert dooder.unique_id == unique_id


def test_dooder_move(dooder):
    object, simulation = dooder
    simulation.environment.move_object(object, (2,2))
    assert object.position == (2,2)


def test_dooder_kill(dooder):
    object, _ = dooder
    other_dooder = mock_dooder()
    object.kill(other_dooder)


def test_dooder_die(dooder):
    dooder = mock_dooder()
    dooder.die()


def test_dooder_choose_random_move(dooder):
    object, _ = dooder
    origin, destination = object.choose_random_move()
    assert origin == (1,1)
    assert destination in [(1,2), (2,1), (2,2), (1,1), (1,0), (0,1), (0,0), (2,0), (0,2), (2,2)]


def test_dooder_step(dooder):
    object, _ = dooder
    object.step()
    
    
def test_death_check(dooder):
    dooder = mock_dooder()
    assert dooder.death_check() == False
    dooder.days_hungry = 3
    dooder.energy_supply = 0
    assert dooder.death_check() == True
    
    
def test_str(dooder):
    dooder, _ = dooder
    assert str(dooder)
