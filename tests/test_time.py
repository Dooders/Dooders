import pytest

from sdk.time import Time
from tests.util import DooderTestObject, EnergyTestObject


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


# def test_time_remove(time = time_with_objects):
#     time.remove(DooderTestObject)
#     time.remove(EnergyTestObject)







