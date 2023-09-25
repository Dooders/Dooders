# import pytest
# from sdk.models import Dooder
# from sdk.utils.mocks import mock_dooder, mock_simulation


# @pytest.fixture
# def dooder():
#     simulation = mock_simulation()
#     unique_id = simulation.generate_id()
#     object = Dooder(unique_id, (1,1), simulation)
#     simulation.environment.place_object(object, (1,1))
#     simulation.time.add(object)
    
#     return object, simulation


# def test_dooder_init():
#     simulation = mock_simulation()
#     unique_id = simulation.generate_id()
#     dooder = Dooder(unique_id, (1,1), simulation)
#     assert dooder.position == (1,1)
#     assert dooder.id == unique_id


# def test_dooder_move(dooder):
#     object, simulation = dooder
#     simulation.environment.move_object(object, (2,2))
#     assert object.position == (2,2)


# def test_dooder_die(dooder):
#     dooder = mock_dooder()
#     dooder.die()


# def test_dooder_step(dooder):
#     object, _ = dooder
#     object.step()
    
    
# def test_str(dooder):
#     dooder, _ = dooder
#     assert str(dooder)
