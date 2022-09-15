import pytest

from sdk.environment import Environment
from tests.test_util import DooderTestObject, EnergyTestObject, mock_simulation

@pytest.fixture
def simulation():
    simulation = mock_simulation()
    simulation.environment.place_object(DooderTestObject, (1, 1))
    simulation.environment.place_object(EnergyTestObject, (1, 1))
    return simulation


def test_environment_init():
    simulation = mock_simulation()
    environment = Environment(simulation.params.Environment)


def test_place_object(simulation):
    assert simulation.environment.grid[1][1] == [DooderTestObject, EnergyTestObject]


def test_remove_object(simulation):
    simulation.environment.remove_object(DooderTestObject)
    assert simulation.environment.grid[1][1] == [EnergyTestObject]


def test_move_object(simulation):
    simulation.environment.move_object(DooderTestObject, (1,2))
    assert simulation.environment.grid[1][2] == [DooderTestObject]
    
    
def test_get_object(simulation):
    assert simulation.environment.get_object(DooderTestObject.unique_id) == DooderTestObject
    assert simulation.environment.get_object(EnergyTestObject.unique_id) == EnergyTestObject
    assert simulation.environment.get_object('aaaa') == 'No object found'


def test_get_objects(simulation):
    assert simulation.environment.get_objects() == [DooderTestObject, EnergyTestObject]


def test_iter_neighborhood(simulation):
    neighborhood = list(simulation.environment.iter_neighborhood((1, 1)))
    assert neighborhood == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]


def test_get_neighborhood(simulation):
    assert simulation.environment.get_neighborhood((1, 1)) == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
    # assert simulation.environment.get_neighborhood((0, 0)) == [(0, 1), (0, 9), (1, 0), (1, 1), (1, 9), (9, 0), (9, 1), (9, 9)]


def test_iter_neighbors(simulation):
    neighbors = list(simulation.environment.iter_neighbors((1, 2)))
    assert neighbors == [DooderTestObject, EnergyTestObject]


def test_get_neighbors(simulation):
    neighbors = simulation.environment.get_neighbors((1, 2))
    assert neighbors == [DooderTestObject, EnergyTestObject]


def test_out_of_bounds(simulation):
    assert simulation.environment.out_of_bounds((1, 1)) == False
    assert simulation.environment.out_of_bounds((0, 0)) == False
    assert simulation.environment.out_of_bounds((10, 10)) == True
    assert simulation.environment.out_of_bounds((11, 11)) == True


def test_get_cell_list_contents(simulation):
    assert simulation.environment.get_cell_list_contents((1, 1)) == [DooderTestObject, EnergyTestObject]
    assert simulation.environment.get_cell_list_contents((0, 0)) == []
    assert simulation.environment.get_cell_list_contents((1, 2)) == []


def test_is_cell_empty(simulation):
    assert simulation.environment.is_cell_empty((1, 1)) == False
    assert simulation.environment.is_cell_empty((0, 0)) == True
    assert simulation.environment.is_cell_empty((1, 2)) == True


def test_get_object_types(simulation):
    assert simulation.environment.get_object_types() == ['Dooder', 'Energy']
    
    
# def test_get_random_neighbors(simulation):
#     assert simulation.environment.get_random_neighbors((1, 1)) == DooderTestObject
#     assert simulation.environment.get_random_neighbors((1, 2)) == None
    
    
# def test_get_random_neighborhoods(simulation):
#     assert simulation.environment.get_random_neighborhood((1, 1)) == (0, 0)
#     assert simulation.environment.get_random_neighborhood((1, 2)) == None