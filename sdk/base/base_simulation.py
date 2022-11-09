import random
from abc import ABC, abstractmethod

from sdk.config import ExperimentParameters
from sdk.models import Environment, Information, Time
from sdk.utils import ShortID

# maybe have a dict that contains each simulation component (Environment, etc.)
# Components (Society, Environment) and objects ( Dooders, Energy)
# Still need to figure out how each component and its objects interact with each other


class BaseSimulation(ABC):
    """ 
    """

    def __init__(self, simulation_id: str, experiment_id: str, params: ExperimentParameters):
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
        self.simulation_id = simulation_id
        self.experiment_id = experiment_id
        self.config = self.load_config(params)
        self.random = random
        self.params = ExperimentParameters.parse_obj(self.config)
        self.components = [] #! this will house all the components. Makes it easier to abstract
        
        # Initialize the simulation components
        self.environment = Environment(self.params.Environment)
        self.information = Information(self)
        self.time = Time()
        self.seed = ShortID()
        
        
    def update_config(self, config_change):
        for config in config_change:
            pass
            
            
    def load_config(self, params):
        pass
            

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
