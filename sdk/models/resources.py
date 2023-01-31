"""  
Resources Model
---------------
Responsible for creation and management of Energy objects in the simulation.
"""

from typing import TYPE_CHECKING

from pydantic import BaseModel

from sdk.core import Strategy
from sdk.models.energy import Energy

if TYPE_CHECKING:
    from sdk.simulation import Simulation


class Attributes(BaseModel):
    """ 
    Data model for the Resources class attributes.
    """
    allocated_energy: int = 0
    dissipated_energy: int = 0
    consumed_energy: int = 0


ResourceStrategy = Strategy.load('resources')


class Resources:
    """ 
    Class manages Energy objects in the simulation.
    They are generated and placed based on the selected strategy.

    The class also keeps track of the total number of allocated, dissipated, and 
    consumed energy for each cycle. (The Information class will have historical 
    data for the above stats. The counts are reset after each cycle.)

    Parameters
    ----------
    simulation : Simulation object
        The simulation object that contains the environment, agents, 
        and other models.

    Attributes
    ----------
    simulation: see ``Parameters`` section.
    available_resources : dict
       Current available resources indexed by their unique id.
    allocated_energy : int
        The total number of allocated energy (for the current cycle).
    dissipated_energy : int
        The total number of dissipated energy (for the current cycle).
    consumed_energy : int
        The total number of consumed energy (for the current cycle).
        
    Methods
    -------
    allocate_resources()
        Allocates resources based on the provided strategy.
    step()
        Performs a step in the simulation.
    reset()
        Collects the data from the simulation.
    remove(resource: Energy)
        Consumes the given resource.
    """

    available_resources = {}

    def __init__(self, simulation: 'Simulation') -> None:
        self.simulation = simulation
        self.strategies = Strategy.compile(self, ResourceStrategy)
        self.reset()

    def allocate_resources(self) -> None:
        """ 
        Allocates resources based on the provided strategy.
        
        The method will generate a new Energy object and place it in the
        environment. The Energy object will be added to the available_resources
        dictionary.
        """

        #! add in to do .next() instead of settings resetting every cycle
        #! use placement strategy w/ dooders too?
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
        
        Process
        -------
        1. Calls the step method on each Energy object
        2. Compiles the strategy for the current cycle
        3. Resets the attribute counts from previous cycle
        4. Allocates resources for the current cycle
        
        Notes
        -----
        The Information class will have historical data for attributes after
        each cycle.
        """

        for resource in list(self.available_resources.values()):
            resource.step()

        self.strategies = Strategy.compile(self, ResourceStrategy)
        self.reset()
        self.allocate_resources()

    def reset(self):
        """ 
        Collects the data from the simulation.

        Takes the current total and subtracts the previous total to get 
        the difference. That will be to incremental change since the 
        previous cycle
        """
        for attribute in Attributes():
            setattr(self, attribute[0], attribute[1])

    def remove(self, resource: 'Energy') -> None:
        """ 
        Consumes the given resource.

        Parameters
        ----------
        resource : Energy object
            The Energy object to be removed.
        """
        self.available_resources.pop(resource.unique_id)

    def log(self, granularity: int, message: str, scope: str) -> None:
        """ 
        Logs the given message.

        Parameters
        ----------
        granularity : int
            The granularity of the message. Higher granularity messages will
            be logged less frequently.
        message : str
            The message to log.
        scope : str 
            The scope of the message.
        """
        self.simulation.log(granularity, message, scope)
        