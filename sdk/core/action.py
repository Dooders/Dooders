""" 
Core: Action
------------
This module contains the Action class, 
which is used to register and execute actions.
"""

from typing import Callable


class Actions:
    """ 
    An action is a way for an object to interact with the simulation.
    
    Methods
    -------
    register
        Registers an action to the Actions class.
    
    __call__
        Executes an action.
    """

    actions = {}

    def __init__(self):
        from sdk import actions

    @classmethod
    def register(cls) -> Callable:
        """ 
        Registers an action to the Actions class.
        
        Returns
        -------
        Callable
            A decorator that registers an action to the Actions class.
        """

        def inner_wrapper(wrapped_class: Callable) -> Callable:
            cls.actions[wrapped_class.__name__] = wrapped_class

            return wrapped_class

        return inner_wrapper

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
        matched_action = self.actions[action]
        action_results = matched_action(object)

        return action_results
