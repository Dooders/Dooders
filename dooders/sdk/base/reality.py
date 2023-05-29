import random
from abc import ABC, abstractmethod

import yaml
import ast

# from sdk.config import ExperimentParameters
from dooders.sdk.models import Time
from dooders.sdk.utils import ShortID

# maybe have a dict that contains each simulation component (Environment, etc.)
# Components (Arena, Environment) and objects ( Dooders, Energy)
# Still need to figure out how each component and its objects interact with each other

class Reality(ABC):
    """ 
    """

    def __init__(self):
        """ 
        Args:
            experiment_id: Unique ID for the experiment
            params: Parameters for the experiment

        Attributes:
            experiment_id: Unique ID for the experiment
            params: Parameters for the experiment
            time: Time object for the simulation
            environment: Environment object for the simulation
            components: Dictionary of components for the simulation
        """
        self.seed = ShortID()
        self.simulation_id = self.seed.uuid()
        # self.config = self.load_config(params)
        self.random = random
        # self.params = ExperimentParameters.parse_obj(self.config)

        # Initialize the simulation components
        self.time = Time()
        

    def load_config(self, params):
        with open('sdk/config.yml') as f:
            default_config = yaml.load(f, Loader=yaml.FullLoader)

        if params:
            for k, v in params.items():
                for value in v:
                    default_config[k][value] = params[k][value]

        return default_config
    
    def load_log(self) -> list:
        """ 
        Load the log file for the simulation
        
        Returns:
            A list of dictionaries containing the logs for the simulation
        """
        logs = []
        with open(f"logs/log.json", "r") as f:
            lines = f.readlines()
            for line in lines:
                if self.simulation_id in line:
                    final = line[:-2]
                    logs.append(ast.literal_eval(final))
                    
        return logs

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
