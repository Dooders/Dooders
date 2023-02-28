""" 
Core: Action
------------
This module contains the Action class, 
which is used to register and execute actions.
"""

from typing import Callable

from dooders.sdk.core.core import Core

class Action(Core):
    """ 
    An action is a way for an object to interact with the simulation.
    
    Methods
    -------
    get_action(action_name: str) -> Callable
        Returns all registered actions from the actions directory
    execute(object: object, action_name: str) -> Callable
        Executes a registered action.
    """
        
    def get_action(self, action_name: str) -> Callable:
        """ 
        Returns all registered actions.
        
        Parameters
        ----------
        action_name : str
            The name of the action to get.
            
        Returns
        -------
        Callable
            The action that was requested.
            
        Examples
        --------
        >>> from sdk.core.action import Action
        >>>
        >>> Action.get_action('move')
        <function move at 0x000001E0F1B0F0A0>
        """
        return self.get_component("action", action_name)[action_name]
    
    @classmethod
    def execute(cls, object: object, action_name: str) -> Callable:
        """ 
        Executes a registered action.
        
        Parameters
        ----------
        object : Object, (Dooder, Energy, etc.)
            The object that is executing the action.
        action : str, (move, consume, etc.)
            The name of the action to execute.
            
        Returns
        -------
        Callable
            The action that was executed.
            
        Examples
        --------
        >>> from sdk.core.action import Action
        >>> from sdk.objects.dooder import Dooder
        >>>
        >>> Action.execute(Dooder(0, 0), 'move')
        <function move at 0x000001E0F1B0F0A0>
        """
        matched_action = cls.get_action(cls, action_name)
        action_results = matched_action.function(object)

        return action_results
