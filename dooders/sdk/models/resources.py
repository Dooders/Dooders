"""  
Resources Model
---------------
Responsible for creation and management of Energy objects in the simulation.
"""

from typing import TYPE_CHECKING

from pydantic import BaseModel

from dooders.sdk.core.settings import Settings
from dooders.sdk.core.strategy import Strategy
from dooders.sdk.models.energy import Energy

if TYPE_CHECKING:
    from dooders.sdk.simulation import Simulation


class Attributes(BaseModel):
    """ 
    Data model for the Resources class attributes.
    """
    allocated_energy: int = 0
    dissipated_energy: int = 0
    consumed_energy: int = 0


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

    def __init__(self, simulation: 'Simulation', settings) -> None:
        self.simulation = simulation
        self.settings = settings

    def _setup(self) -> None:
        """ 
        Sets up the Resources class.

        The method will allocate resources based on the strategy.
        """
        self.reset()

    def allocate_resources(self) -> None:
        """ 
        Allocates resources based on the provided strategy.

        The method will generate a new Energy object and place it in the
        environment. The Energy object will be added to the available_resources
        dictionary.
        """
        energy_count = self.EnergyPerCycle()
        for location in self.EnergyPlacement(energy_count):
            if len(self.available_resources) < self.MaxTotalEnergy():
                energy = self.create_energy(location)
                self.simulation.environment.place_object(energy, location)
                self.available_resources[energy.id] = energy
                self.allocated_energy += 1

    def create_energy(self, location):
        unique_id = self.simulation.generate_id()
        settings = Settings.get('variables')['energy']
        energy = Energy(unique_id, location, self)
        Strategy.compile(energy, settings)

        return energy

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
        self.available_resources.pop(resource.id)
        self.consumed_energy += 1
        del resource

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

    @property
    def average_energy_age(self) -> int:
        """ 
        Returns the average age of the available energy.

        Returns
        -------
        int
            The average age of the available energy.
        """
        try:
            return round(sum([energy.age for energy in self.available_resources.values()]) / len(self.available_resources), 3)
        except ZeroDivisionError:
            return 0

    def collect(self):
        """ 
        Returns the data to be collected.

        Returns
        -------
        dict
            The data to be collected.
        """
        return {
            'available_energy': len(self.available_resources),
            'allocated_energy': self.allocated_energy,
            'consumed_energy': self.consumed_energy,
            'average_energy_age': self.average_energy_age,
        }
