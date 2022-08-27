from abc import ABC, abstractmethod
import random


class BaseObject(ABC):
    def __init__(self, unique_id: int, position, simulation) -> None:
        """
        Object Meta-Class
        """
        self.unique_id = unique_id
        self.simulation = simulation
        self.position = position
        self.environment = simulation.environment
        self.information = simulation.information

    def log(self, granularity: int, message: str, scope: str) -> None:
        # get specific dooder instance details and send to information object
        cycle_number = self.simulation.time.time

        log_dict = {
            'scope': scope,
            'id': self.unique_id,
            'cycle_number': cycle_number,
            'granularity': granularity,
            'message': message
        }

        # final_message = f"'{scope}' - '{self.unique_id}' - '{cycle_number}' - '{granularity}' - '{message}'"

        final_message = str(log_dict).strip('{}')
        
        self.information.log(final_message, granularity)

    @abstractmethod
    def step(self) -> None:
        pass

    @property
    def random(self) -> random.Random:
        return self.simulation.random
    
    @property
    def name(self) -> str:
        return self.__class__.__name__