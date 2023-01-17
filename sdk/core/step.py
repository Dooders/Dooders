""" 
Step Core
---------
"""

from abc import ABC, abstractmethod


class Step:
    """ 
    This will be responsible for registering step flows
    
    A step is a point in the simulation to execute logic 
    for a specific object or model during its turn.
    
    In decorator state the model
    
    Might need the class below and go to a class decorator, rather than a
    function decorator
    
    Step plan is the selection for the step functions
    """
    pass

class StepFlow(ABC):
    """ 
    Might not need this class after all
    """
    
    @abstractmethod
    def react(self):
        pass
    
    @abstractmethod
    def act(self):
        pass
