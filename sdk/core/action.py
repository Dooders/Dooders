""" 
Core: Action
------------
This module contains the Action class, 
which is used to register and execute actions.
"""

from typing import Callable

from sdk.core import CoreComponent


class Action(CoreComponent):
    """ 
    An action is a way for an object to interact with the simulation.
    
    Methods
    -------
    register
        Registers an action to the Actions class.
    
    __call__
        Executes an action.
    """
    
    def __init__(self):
        from sdk import actions
        
    def get_action(self, action_name: str) -> Callable:
        """ 
        Returns all registered actions.
        
        Parameters
        ----------
        action_name : str
            The name of the action to get.
        """
        return self.get_component("sdk.actions", action_name)[action_name]
    
    @classmethod
    def execute(cls, object: object, action_name: str) -> Callable:
        """ 
        Executes a registered action.
        
        Parameters
        ----------
        object : Object
            The object that is executing the action.
        action : str
            The name of the action to execute.
            
        Returns
        -------
        Callable
            The action that was executed.
        """
        matched_action = cls.get_action(cls, action_name)
        action_results = matched_action.function(object)

        return action_results
