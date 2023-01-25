""" 
Core: Step
----------
Core system for the Step Logic
"""

from abc import ABC, abstractmethod
from typing import Callable

#! Consistent plugin schema for every component
#! Base class handles a lot
#! Add methods to docstrings, and examples
#! fix the importing strategy so its consistent across components
#! Add better descriptions to the docstrings
#! should I rename registry and make it consistent? Would be in baseclass


class Step:
    """ 
    A step is a point in the simulation to execute logic 
    for a specific object or model during its turn.
    
    Attributes
    ----------
    registry : dict
        A dictionary of all the registered step flows, 
        by the type of python object
        
    Methods
    -------
    register(type: str) -> Callable
        Register a step flow through a decorator
    forward(name: str, object: str) -> None
        Execute a step flow
    """
    #! make this a dataclass above
    registry = {
        'Dooder': {},
        'Environment': {},
        'Resource': {},
    }
    
    @classmethod
    def register(cls, type: str) -> Callable:
        """ 
        Register a step flow through a decorator
        
        Parameters
        ----------
        type : str
            The type of python object to register the step flow for
            For example, 'Dooder' or 'Environment'
            
        Returns
        -------
        Callable
            The decorator to register the step flow
        """
        
        def inner_wrapper(wrapped_class: Callable) -> Callable:
            cls.registry[type][wrapped_class.__name__] = wrapped_class
            
            return wrapped_class
        
        return inner_wrapper
    
    @classmethod
    def forward(cls, name: str, object: str) -> None:
        """ 
        Execute a step flow
        
        Parameters
        ----------
        name : str
            The name of the step flow to execute
        object : object
            The object to execute the step flow on
        """
        step_flow = cls.registry[object.__class__.__name__][name]
        step_flow.step(object)


class StepLogic(ABC):
    """ 
    Abstract Class for every step flow
    """
    __model__ = ''
    __name__ = ''
    
    def react(self, *args, **kwargs) -> None:
        """ 
        Optional method to react to the environment before acting
        
        Parameters
        ----------
        object : object
            The object that needs to react before acting
        """
        pass
    
    @abstractmethod
    def act(self, *args, **kwargs) -> None:
        """ 
        Required method to execute the action phase of the step flow
        
        Parameters
        ----------
        object : object
            The object that needs to act. Passed during the objects turn
        """
        raise NotImplementedError('act method not implemented')
    
    def sleep(self, *args, **kwargs) -> None:
        """ 
        Optional method to sleep after acting
        
        Parameters
        ----------
        object : object
            The object that needs to sleep after acting
        """
        pass
    
    @classmethod
    def step(cls, object: object) -> None:
        """ 
        Execute the step flow

        Parameters
        ----------
        object : object
            The object to execute the step flow on
        """
        cls.react(object)
        cls.act(object)
        cls.sleep(object)
    
