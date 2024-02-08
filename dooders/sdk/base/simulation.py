from abc import ABC, abstractmethod
from dooders.sdk.utils.short_id import seed

class Simulation(ABC):
    def __init__(self, settings):
        self.id = seed.uuid()
        self.settings = settings
        self.running = False
        self.cycle_number: int = 0
        self.results = {}

    @abstractmethod
    def setup(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def run_simulation(self, step_count: int) -> None:
        pass

    def cycle(self) -> None:
        self.cycle += 1
        self.cycle_number += 1
        self.update()

    def reset(self) -> None:
        self.cycle_number = 0
        self.results = {}

    def stop(self) -> None:
        self.running = False

    @property
    def state(self) -> dict:
        #! represents the object data
        pass

    @property
    def generate_id(self) -> str:
        return seed.uuid()
