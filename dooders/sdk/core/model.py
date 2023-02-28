""" 
Core: Model
-----------
This module contains the Model class, 
which is used to register and execute models.
"""

from abc import ABC
from functools import partial

from dooders.sdk.core import Strategy
from dooders.sdk.utils.types import Settings

#! Is this still needed????
class Model(ABC):
    
    def __init__(self, simulation):
        self.simulation = simulation
    
    @classmethod
    def from_settings(cls, simulation, settings: 'Settings') -> 'Model':
        """ 
        Setup the model from the settings dictionary
        """
        for variable in settings:
            func = Strategy.get(settings[variable]['function'])
            partial_func = partial(func, **settings[variable]['args'])
            setattr(cls, variable, partial_func)
            
        return cls(simulation)
    
    def step(self):
        """ 
        Optional method that executes the logic for a 
        single step of the model during a cycle in the simulation
        
        A step is a single iteration of the model's logic that
        occurs during a cycle in the simulation.
        """
        pass
    
    def setup(self):
        """ 
        Optional method for any actions that need to occur 
        at the beginning of the simulation before the first cycle
        """
        pass
    
    def teardown(self):
        """ 
        Optional method for any actions that need to occur at 
        the end of the simulation
        
        Like aggregating model data, saving state, etc.
        """
        pass
   
