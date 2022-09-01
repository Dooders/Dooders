import pytest
import sys
sys.path.append('C:\\Users\\peril\\Dropbox\\Dooders\\')
sys.path.append('D:\\Dropbox\\Dooders\\')


from sdk.information import Information
from util import simulation


@pytest.fixture
def information():
    information = Information('1')
    return information


def test_information_init(information):
    information = Information('1')
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

