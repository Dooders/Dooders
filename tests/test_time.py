import pytest

from sdk.time import Time
from tests.test_util import DooderTestObject, EnergyTestObject
from sdk.dooder import Dooder
from sdk.environment import Energy


@pytest.fixture
def time():
    return Time()

@pytest.fixture
def time_with_objects(time):
    time.add(DooderTestObject)
    time.add(EnergyTestObject)
    return time


def test_time_init():
    time = Time()
    assert time.steps == 0


def test_time_add(time):
    time.add(DooderTestObject)
    time.add(EnergyTestObject)
    
    
def test_time_step(time_with_objects):
    time_with_objects.step()
    assert time_with_objects.steps == 1
    assert time_with_objects.time == 1
    
    
# def test_get_object_count(time_with_objects):
#     assert time_with_objects.get_object_count(Dooder) == 1
#     assert time_with_objects.get_object_count(Energy) == 1
    
    
# def test_time_get_object(time_with_objects):
#     assert time_with_objects.get_object(Dooder, 1) == DooderTestObject
#     assert time_with_objects.get_object(Energy, 2) == EnergyTestObject


# def test_time_remove(time = time_with_objects):
#     time.remove(DooderTestObject)
#     time.remove(EnergyTestObject)







