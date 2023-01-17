""" 
Model Core
----------
"""

from abc import ABC, abstractmethod

class CoreModel(ABC):
    
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
    
    
class Model:
    """ 
    Register all models in the models directory
    """
    pass