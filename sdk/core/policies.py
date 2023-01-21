""" 
Core: Policies
--------------
This module contains the Policies class,
which is used to register and execute policies.
"""

from typing import Callable

class Policies:
    """ 
    The factory class to be used as a decorator to register a policy.
    
    Methods
    -------
    register
        Registers a policy to the Policies class.
    __call__
        Executes a policy.
    """

    policies = {}
    
    def __init__(self) -> None:
      from sdk import policies

    @classmethod
    def register(cls) -> Callable:
        """ 
        Registers a policy to the Policies class.
        
        Returns
        -------
        Callable
            A decorator that registers a policy to the Policies class.
        """

        def inner_wrapper(wrapped_class: Callable) -> Callable:
            cls.policies[wrapped_class.__name__] = wrapped_class

            return wrapped_class

        return inner_wrapper
    
    def __call__(self, policy: str, *args, **kwargs) -> Callable:
        """ 
        Executes a registered policy.
        
        Parameters
        ----------
        policy : str
            The name of the policy to execute.
        
        Returns
        -------
        Callable
            The results of the policy
        """
        matched_policy = self.policies[policy]
        policy_results = matched_policy.execute(*args, **kwargs)
        
        return policy_results
