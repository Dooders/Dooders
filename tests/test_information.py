import pytest


from sdk.information import Information
from tests.test_util import simulation


@pytest.fixture
def information():
    information = Information('1', simulation.params.Information)
    return information


def test_information_init(information):
    information = Information('1', simulation.params.Information)
    assert information.experiment_id == '1'


def test_information_collect(information):
    information.collect(simulation)
    
    
def test_add_collector(information):
    
    def test_function():
        return 'This worked'
    
    collector = {'name': "TestFunction", 'function': test_function, 'component': "Simulation"}
    information._add_collector(collector)
    assert information.collectors['Simulation']['TestFunction'] == test_function
    assert information.data['Simulation']['TestFunction'] == []
        
        
def test_information_get_dataframe(information):
    information.collect(simulation)
    assert information.get_dataframe('Simulation') is not None


def test_collect(information):
    information.collect(simulation)
    assert len(information.data) > 0
    
    
def test_read_log(information):
    assert information.read_log()
    
    
def test_get_experiment_log(information):
    assert information.get_experiment_log()