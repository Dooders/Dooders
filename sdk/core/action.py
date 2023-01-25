""" 
Core: Action
------------
This module contains the Action class, 
which is used to register and execute actions.
"""

from typing import Callable

from sdk.core.core import Core


class Actions(Core):
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
    
    #! change to execute?
    def __call__(self, object: object, action: str) -> Callable:
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
        matched_action = self.get_component_dict("sdk.actions", action)[action]
        action_results = matched_action.func(object)

        return action_results
