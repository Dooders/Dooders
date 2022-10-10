import yaml
from sdk.models.dooder import Dooder
from sdk.models.energy import Energy
from sdk.simulation import Simulation
from sdk.models.resources import Resources

#! do i need a test config?

# with open("sdk/config.json", "r") as f:
#      test_config = json.load(f)
     
with open('sdk/config.yml') as f:
    test_config = yaml.load(f, Loader=yaml.FullLoader)


simulation = Simulation('test', test_config)

def mock_simulation():
    return Simulation('test', test_config)

DooderTestObject = Dooder(1, (1, 1), simulation)
EnergyTestObject = Energy(2, (1, 1), Resources)
