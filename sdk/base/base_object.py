import random
from abc import ABC, abstractmethod


class BaseObject(ABC):
    """ 

    """

    def __init__(self, unique_id: int, position, simulation) -> None:
        """
        Object Meta-Class

        Args:
            unique_id: Unique ID for the object
            position: Position of the object
            simulation: Simulation object for the object

        Attributes:
            unique_id: Unique ID for the object
            position: Position of the object
            simulation: Simulation object for the object
            information: Information object for the object
            environment: Environment object for the object
        """
        self.unique_id = unique_id
        self.simulation = simulation
        self.position = position
        self.environment = simulation.environment
        self.information = simulation.information

    def log(self, granularity: int, message: str, scope: str) -> None:
        """ 
        Log a message to the information object

        Args:
            granularity: Granularity of the log
            message: Message to log
            scope: Scope of the log
        """
        cycle_number = self.simulation.time.time

        log_dict = {
            'Scope': scope,
            'UniqueID': self.unique_id,
            'CycleNumber': cycle_number,
            'Granularity': granularity,
            'Message': message
        }

        final_message = str(log_dict).strip('{}')

        self.information.log(final_message, granularity)

    @abstractmethod
    def step(self) -> None:
        pass

    @property
    def random(self) -> random.Random:
        """  
        Returns:
            Random object for the simulation
        """
        return self.simulation.random

    @property
    def name(self) -> str:
        """ 
        Returns:
            Name of the object
        """
        return self.__class__.__name__
