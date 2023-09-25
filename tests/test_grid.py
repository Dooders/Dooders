# import pytest

# from sdk.surfaces.grid import Grid

# settings = {'height':10, 'width':10, 'torus': True}


# @pytest.fixture
# def grid():
#     grid = Grid(settings)
#     grid.add(TestObject(1), (0,0))
#     grid.add(TestObject(2), (1,1))
    
#     return grid

# class TestObject:
    
#     def __init__(self, id):
#         self.id = id
#         self.id = 'test_id'

# def test_init():
#     grid = Grid(settings)
#     assert grid.height == 10
#     assert grid.width == 10
#     assert grid.torus == True
#     assert len(grid.grid) == 10
#     assert grid._nearby_cache == {}
    
# def test_add_object(grid):
#     test_object = TestObject(3)
#     grid.add_object(test_object, (0,0))
#     assert grid.grid[0][0].contents[test_object.id] == test_object
#     assert test_object.position == (0,0)
    
# def test_remove_object(grid):
#     test_object = grid.grid[0][0].contents[1]
#     grid.remove_object(test_object)
#     assert grid.grid[0][0].is_empty == True
    
# def test_remove_object_from_id(grid):
#     test_object = grid.grid[0][0].contents[1]
#     grid.remove(test_object.id)
#     assert grid.grid[0][0].is_empty == True

# def test_coordinates(grid):
#     assert type(grid.coordinates()) == list
#     for coord in grid.coordinates():
#         assert type(coord) == tuple
#         assert coord == (0,0)
#         assert len(coord) == 2
#         assert type(coord[0]) == int
#         assert type(coord[1]) == int
#         break
    
# def test_spaces(grid):
#     assert type(grid.spaces()) == list
#     for space in grid.spaces():
#         assert space.position == (0,0)
#         break
    
# def test_contents(grid):
#     assert type(grid.contents()) == list
#     for contents in grid.contents():
#         assert type(contents) == dict
#         break
    
# def test_contents_by_type(grid):
#     assert type(grid.contents('TestObject')) == list
#     for contents in grid.contents('TestObject'):
#         assert type(contents) == dict
#         break
    
# def test_nearby_spaces(grid):
#     assert type(grid.nearby_spaces((0,0))) == list
#     for space in grid.nearby_spaces((0,0)):
#         assert space.position == (0,0)
#         break
# def test_nearby_contents(grid):
#     assert type(grid.nearby_contents((0,0))) == list
#     for contents in grid.nearby_contents((0,0)):
#         assert type(contents) == dict
#         break
    
# def test_nearby_coordinates(grid):
#     assert type(grid.nearby_coordinates((0,0))) == list
#     for coord in grid.nearby_coordinates((0,0)):
#         assert type(coord) == tuple
#         assert coord == (0,0)
#         assert len(coord) == 2
#         assert type(coord[0]) == int
#         assert type(coord[1]) == int
#         break
    
# def test_get(grid):
#     assert type(grid[0]) == list
#     assert len(grid[0]) == 10
#     assert grid[[(0,0)]].position == (0,0)
#     assert grid[(0,0)].position == (0,0)
#     assert grid[0,0].position == (0,0)
#     assert grid[0][0].position == (0,0)
#     assert len(grid['all']) == 2
#     assert type(grid['all']) == list