import yaml
from sdk.dooder.dooder import Dooder
from sdk.environment.energy import Energy
from sdk.simulation import Simulation


# with open("sdk/config.json", "r") as f:
#      test_config = json.load(f)
     
with open('sdk/config.yml') as f:
    test_config = yaml.load(f, Loader=yaml.FullLoader)


simulation = Simulation('test', test_config)

def mock_simulation():
    return Simulation('test', test_config)

DooderTestObject = Dooder(1, (1, 1), simulation, simulation.params.Dooder)
EnergyTestObject = Energy(2, (1, 1), simulation, simulation.params.Energy)