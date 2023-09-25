# import pytest


# from sdk.models import Information
# from tests.test_util import simulation


# @pytest.fixture
# def information():
#     information = Information(simulation)
#     return information


# def test_information_init(information):
#     assert Information(simulation)


# def test_information_collect(information):
#     information.collect(simulation)
    
    
# def test_add_collector(information):
#     #! Need to update
#     # def test_function():
#     #     return 'This worked'
    
#     # collector = {'name': "TestFunction", 'function': test_function, 'component': "Simulation"}
#     # information._add_collector(collector)
#     # assert information.collectors['Simulation']['TestFunction'] == test_function
#     # assert information.data['Simulation']['TestFunction'] == []
#     pass
        
        
# def test_information_get_dataframe(information):
#     information.collect(simulation)
#     assert information.get_dataframe('simulation') is not None


# def test_collect(information):
#     information.collect(simulation)
#     assert len(information.data) > 0
    
    
# def test_read_log(information):
#     assert information.read_log()
    
    
# def test_get_experiment_log(information):
#     assert information.get_experiment_log()
    
    
# def test_collectors(information):
#     assert information.collectors is not None