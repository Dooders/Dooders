import pytest
import sys
sys.path.append('C:\\Users\\peril\\Dropbox\\Dooders\\')
sys.path.append('D:\\Dropbox\\Dooders\\')


from sdk.environment import Environment
from sdk.tests.util import DooderTestObject, EnergyTestObject
from sdk.parameters import ExperimentParameters

@pytest.fixture
def env():
    env = Environment(ExperimentParameters['Environment'])
    env.place_object(DooderTestObject, (1, 1))
    env.place_object(EnergyTestObject, (1, 1))
    return env


def test_place_object(env):
    assert env.grid[1][1] == [DooderTestObject, EnergyTestObject]


def test_remove_object(env):
    env.remove_object(DooderTestObject)
    assert env.grid[1][1] == [EnergyTestObject]


def test_move_object(env):
    env.move_object(DooderTestObject, (1,2))
    assert env.grid[1][2] == [DooderTestObject]


def test_get_objects(env):
    assert env.get_objects() == [DooderTestObject, EnergyTestObject]


def test_iter_neighborhood(env):
    neighborhood = list(env.iter_neighborhood((1, 1)))
    assert neighborhood == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]


def test_get_neighborhood(env):

    assert env.get_neighborhood((1, 1)) == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
    assert env.get_neighborhood((0, 0)) == [(0, 1), (0, 9), (1, 0), (1, 1), (1, 9), (9, 0), (9, 1), (9, 9)]


def test_iter_neighbors(env):
    neighbors = list(env.iter_neighbors((1, 2)))
    assert neighbors == [DooderTestObject, EnergyTestObject]


def test_get_neighbors(env):
    neighbors = env.get_neighbors((1, 2))
    assert neighbors == [DooderTestObject, EnergyTestObject]


def test_out_of_bounds(env):
    assert env.out_of_bounds((1, 1)) == False
    assert env.out_of_bounds((0, 0)) == False
    assert env.out_of_bounds((10, 10)) == True
    assert env.out_of_bounds((11, 11)) == True
    assert env.out_of_bounds((-1, -1)) == True
    assert env.out_of_bounds((-10, -10)) == True
    assert env.out_of_bounds((-11, -11)) == True
    assert env.out_of_bounds((12, 12)) == True
    assert env.out_of_bounds((-12, -12)) == True
    assert env.out_of_bounds((-12, 12)) == True
    assert env.out_of_bounds((12, -12)) == True


def test_get_cell_list_contents(env):
    assert env.get_cell_list_contents((1, 1)) == [DooderTestObject, EnergyTestObject]
    assert env.get_cell_list_contents((0, 0)) == []
    assert env.get_cell_list_contents((1, 2)) == []


def test_is_cell_empty(env):
    assert env.is_cell_empty((1, 1)) == False
    assert env.is_cell_empty((0, 0)) == True
    assert env.is_cell_empty((1, 2)) == True
