import pytest

from sdk.dooder.dooder import Dooder
from sdk.environment.energy import Energy
from sdk.simulation import Simulation
from sdk.parameters import ExperimentParameters

# @pytest.fixture
# def simulation():
#     return Simulation('test', DEFAULT_PARAMETERS)

simulation = Simulation('test', ExperimentParameters)

def mock_simulation():
    return Simulation('test', ExperimentParameters)

DooderTestObject = Dooder(1, (1, 1), simulation, ExperimentParameters['Dooder'])
EnergyTestObject = Energy(2, (1, 1), simulation, ExperimentParameters['Energy'])