import sys
sys.path.append('C:\\Users\\peril\\Dropbox\\Dooders\\')
sys.path.append('D:\\Dropbox\\Dooders\\')
sys.path.append('C:\\Users\\peril\\Dropbox\\Dooders\\tests')
sys.path.append('D:\\Dropbox\\Dooders\\tests')
import pytest

from sdk.dooder import Dooder
from util import mock_simulation


@pytest.fixture
def dooder():
    simulation = mock_simulation()
    object = Dooder('1', (1,1), simulation, simulation.params.Dooder)
    simulation.environment.place_object(object, (1,1))
    simulation.time.add(object)
    
    return object, simulation


def test_dooder_init():
    simulation = mock_simulation()
    dooder = Dooder('1', (1,1), simulation, simulation.params.Dooder)
    assert dooder.position == (1,1)
    assert dooder.energy == 5
    assert dooder.unique_id == '1'


def test_dooder_move(dooder):
    object, simulation = dooder
    simulation.environment.move_object(object, (2,2))
    assert object.position == (2,2)


def test_dooder_kill(dooder):
    object, simulation = dooder
    object.kill(object)
    assert object not in simulation.environment.get_objects(Dooder)
    assert object not in simulation.time.get_objects(Dooder)


def test_dooder_die(dooder):
    object, simulation = dooder
    object.die()
    assert object not in simulation.environment.get_objects(Dooder)
    assert object not in simulation.time.get_objects(Dooder)

def test_dooder_choose_random_move(dooder):
    object, _ = dooder
    origin, destination = object.choose_random_move()
    assert origin == (1,1)
    assert destination in [(1,2), (2,1), (2,2), (1,1), (1,0), (0,1), (0,0), (2,0), (0,2), (2,2)]

def test_dooder_step(dooder):
    object, _ = dooder
    object.step()