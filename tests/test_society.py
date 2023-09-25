# import pytest

# from sdk.models.arena import Arena
# from sdk.utils.mocks import mock_simulation


# @pytest.fixture
# def arena():
#     simulation = mock_simulation()
#     arena = Arena(simulation)
    
#     return arena, simulation


# def test_init():
#     simulation = mock_simulation()
#     assert Arena(simulation)


# def test_generate_seed_population(arena):
#     arena, _ = arena
#     arena.generate_seed_population()
#     assert arena.active_dooders != {}
#     assert arena.dooders_created > 0
    
    
# def test_generate_dooder(arena):
#     arena, _ = arena
#     arena.generate_dooder((1,1))
#     assert arena.active_dooders != {}
#     assert arena.dooders_created > 0


# def test_place_dooder(arena):
#     arena, simulation = arena
#     arena.generate_dooder((1,1))
#     assert simulation.environment.grid[1][1] != None
    
    
# # def test_properties():
# #     simulation = mock_simulation()
# #     arena = Arena(simulation)
# #     assert arena.active_dooders == {}
# #     assert arena.total_created_dooders == 0
# #     assert arena.graveyard == {}
# #     assert arena.graph != None
    
# #! need to make this work
# # def test_terminate_dooder(arena):
# #     arena, simulation = arena
# #     arena.generate_dooder((1,1))
# #     dooder = simulation.environment.get_dooder((1,1))
# #     arena.terminate_dooder(dooder)
# #     assert simulation.environment.grid[1][1] == None