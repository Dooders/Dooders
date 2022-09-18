""" 
Resources
---------
This module contains the resources allocated in the environment and used by the
agents. It also contains the functions to access the resources.
"""

from typing import TYPE_CHECKING

from sdk.environment.energy import Energy
from sdk.strategies.strategies import compile_strategy, BaseStrategy

if TYPE_CHECKING:
    from sdk.simulation import Simulation

class ResourceStrategy:
    EnergyPerCycle = BaseStrategy(StrategyType='Generation', 
                                  StrategyFunc='uniform_distribution',
                                  Args={'low': 10, 'high': 15})
    
    MaxTotalEnergy = BaseStrategy(StrategyType='Generation', 
                                  StrategyFunc='normal_distribution',
                                  Args={'mean': 50, 'std': 10})
    
    EnergyPlacement = BaseStrategy(StrategyType='Placement', 
                                   StrategyFunc='random_location',
                                   Args=None, 
                                   Dependency='EnergyPerCycle')
    
    
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
        compile_strategy(self, ResourceStrategy)
    
    def allocate_resources(self):
        """ 
        Allocates resources based on the provided strategy.
        
        Returns:
            The number of allocated resources.
        """
        
        for location in next(self.EnergyPlacement):
            if len(self.available_resources) < next(self.MaxTotalEnergy):
                unique_id = self.simulation.generate_id()
                energy = Energy(unique_id, location, self)
                self.simulation.environment.place_object(energy, location)
                self.available_resources[unique_id] = energy
                self.total_allocated_energy += 1
                
    def step(self):
        """ 
        Performs a step in the simulation.
        """
        
        for resource in list(self.available_resources.values()):
            resource.step()
            
        compile_strategy(self, ResourceStrategy)   
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
        