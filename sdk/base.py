import random
from abc import ABC, abstractmethod
from typing import Dict

from sdk.environment import Environment
from sdk.information import Information
from sdk.parameters import ExperimentParameters
from sdk.time import Time
from sdk.util import ShortUUID

# maybe have a dict that contains each simulation component (Envirnoment, etc.)
# Components (Society, Environment) and objects ( Dooders, Energy)
# Still need to figure out how each compinent and its objects interact with each other


class BaseSimulation(ABC):

    def __init__(self, experiment_id: int, params: ExperimentParameters):
        self.experiment_id = experiment_id
        self.random = random
        self.params = ExperimentParameters

        # Initialize the simulation components
        self.environment = Environment(params['Environment'])
        self.information = Information(experiment_id)
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
