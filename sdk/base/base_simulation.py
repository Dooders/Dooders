import random
from abc import ABC, abstractmethod
from typing import Dict

from sdk.config import ExperimentParameters
from sdk.environment import Environment
from sdk.information import Information
from sdk.time import Time
from sdk.util import ShortUUID

# maybe have a dict that contains each simulation component (Environment, etc.)
# Components (Society, Environment) and objects ( Dooders, Energy)
# Still need to figure out how each component and its objects interact with each other


class BaseSimulation(ABC):
    """ 
    """

    def __init__(self, experiment_id: int, params: ExperimentParameters):
        """ 
        Args:
            experiment_id: Unique ID for the experiment
            params: Parameters for the experiment
            
        Attributes:
            experiment_id: Unique ID for the experiment
            params: Parameters for the experiment
            time: Time object for the simulation
            environment: Environment object for the simulation
            information: Information object for the simulation
            components: Dictionary of components for the simulation
        """
        self.experiment_id = experiment_id
        self.random = random
        self.params = ExperimentParameters.parse_obj(params)
        self.components = [] #! this will house all the components. Makes it easier to abstract
        
        # Initialize the simulation components
        self.environment = Environment(self.params.Environment)
        self.information = Information(self)
        self.time = Time()
        self.seed = ShortUUID()

    @abstractmethod
    def setup(self) -> None:
        pass

    @abstractmethod
    def cycle(self) -> None:
        pass

    @abstractmethod
    def run_simulation(self, step_count: int) -> None:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass
