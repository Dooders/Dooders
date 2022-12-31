""" 
Resources
---------
This module contains the resources allocated in the environment and used by the
agents. It also contains the functions to access the resources.
"""

from typing import TYPE_CHECKING

from pydantic import BaseModel

from sdk.core import Strategy, compile_strategy
from sdk.models.energy import Energy

if TYPE_CHECKING:
    from sdk.simulation import Simulation


class Attributes(BaseModel):
    allocated_energy: int = 0
    dissipated_energy: int = 0
    consumed_energy: int = 0


ResourceStrategy = Strategy.load_strategy('resources')


class Resources:
    """ 
    Resources are the objects that are consumed by agents to perform actions.
    They are generated and placed in random locations based on the provided strategy.

    Args:
    simulation : Simulation object
        The simulation object that contains the environment and the agents.

    Attributes:
        simulation: see ``Args`` section.
        available_resources (dict): A dictionary of *current* available resources indexed by their unique id.
        allocated_energy (int): The total number of allocated resources.
    """

    available_resources = {}

    def __init__(self, simulation: 'Simulation') -> None:
        self.simulation = simulation
        self.strategies = compile_strategy(self, ResourceStrategy)
        self.reset()

    def allocate_resources(self) -> None:
        """ 
        Allocates resources based on the provided strategy.

        Returns:
            The number of allocated resources.
        """

        for location in self.EnergyPlacement:
            if len(self.available_resources) < self.MaxTotalEnergy:
                unique_id = self.simulation.generate_id()
                energy = Energy(unique_id, location, self)
                self.simulation.environment.place_object(energy, location)
                self.available_resources[unique_id] = energy
                self.allocated_energy += 1

    def step(self) -> None:
        """ 
        Performs a step in the simulation.
        """

        for resource in list(self.available_resources.values()):
            resource.step()

        self.strategies = compile_strategy(self, ResourceStrategy)
        self.allocate_resources()
        self.reset()

    def reset(self):
        """ 
        Collects the data from the simulation.

        Takes the current total and subtracts the previous total to get the difference. That will be to incremental change since the previous cycle
        """
        for attribute in Attributes():
            setattr(self, attribute[0], attribute[1])

    def remove(self, resource: 'Energy') -> None:
        """ 
        Consumes the given resource.

        Args:
            resource (Energy): The resource to consume.
        """
        self.available_resources.pop(resource.unique_id)

    def log(self, granularity: int, message: str, scope: str) -> None:
        """ 
        Logs the given message.

        Args:
            granularity (str): The granularity of the message.
            message (str): The message to log.
            scope (str): The scope of the message.
        """
        self.simulation.log(granularity, message, scope)
