""" 
Resources
---------
This module contains the resources allocated in the environment and used by the
agents. It also contains the functions to access the resources.
"""

from typing import TYPE_CHECKING

from sdk.environment.energy import Energy
from sdk.strategies.strategies import Strategies

if TYPE_CHECKING:
    from sdk.simulation import Simulation

strategy = {
    'EnergyPerCycle': {'function': 'uniform_distribution', 'args': {'low': 10, 'high': 15}},
    'MaxTotalEnergy': {'function': 'normal_distribution', 'args': {'mean': 50, 'std': 10}},
    'EnergyLifespan': {'function': 'fixed_value', 'args': {'value': 10}},
    'EnergyPlacement': {'function': 'random_location'}
}

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
        total_allocated_energy (int): The total number of allocated resources.
    """
    
    available_resources = {}
    total_allocated_energy = 0
    
    def __init__(self, simulation: 'Simulation'):
        self.simulation = simulation

    def generation_strategy(self, variable: str):
        """ 
        Generates a value for the given variable based on the provided strategy.
        
        Args:
            variable (str): The name of the variable to generate a value for.
        
        Returns:
            The generated value.
        """
        strat = strategy[variable]['function']
        args = strategy[variable]['args']
        func = Strategies.get(strat, 'Generation')
        
        return round(func(**args))

    def placement_strategy(self, simulation: 'Simulation', number: int):
        """ 
        Generates a list of locations for the given number of resources and based on the provided strategy.
        
        Args:
            simulation (Simulation): The simulation object that contains the environment and the agents.
            number (int): The number of resources to generate locations for.
        
        Returns:   
            A list of locations.
        """
        strat = strategy['EnergyPlacement']['function']
        func = Strategies.get(strat, 'Placement')
        args = (simulation, number)

        return func(*args)
    
    def allocate_resources(self):
        """ 
        Allocates resources based on the provided strategy.
        
        Returns:
            The number of allocated resources.
        """
        energy_per_cycle = self.generation_strategy('EnergyPerCycle')
        max_total_energy = self.generation_strategy('MaxTotalEnergy')
        energy_lifespan = self.generation_strategy('EnergyLifespan')
        energy_placement = self.placement_strategy(self.simulation, energy_per_cycle)
        
        for location in energy_placement:
            if len(self.available_resources) < max_total_energy:
                unique_id = self.simulation.generate_id()
                energy = Energy(unique_id, energy_lifespan, location, self)
                self.simulation.environment.place_object(energy, location)
                self.available_resources[unique_id] = energy
                self.total_allocated_energy += 1
                
    def step(self):
        """ 
        Performs a step in the simulation.
        """
        for resource in list(self.available_resources.values()):
            resource.step()
            
        self.allocate_resources()
            
    def consume(self, resource: Energy):
        """ 
        Consumes the given resource.
        
        Args:
            resource (Energy): The resource to consume.
        """
        self.simulation.environment.remove_object(resource)
        self.available_resources.pop(resource.unique_id)
        
    def log(self, granularity: int, message: str, scope: str):
        """ 
        Logs the given message.
        
        Args:
            granularity (str): The granularity of the message.
            message (str): The message to log.
            scope (str): The scope of the message.
        """
        self.simulation.log(granularity, message, scope)
        