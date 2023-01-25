""" 
Core: Policies
--------------
This module contains the Policies class,
which is used to register and execute policies.
"""

from typing import Callable

from sdk.core.core import Core

class Policies(Core):
    """ 
    The factory class to be used as a decorator to register a policy.
    
    Methods
    -------
    register
        Registers a policy to the Policies class.
    __call__
        Executes a policy.
    """
    
    def __init__(self) -> None:
      from sdk import policies
    
    def __call__(self, policy_name: str, *args, **kwargs) -> Callable:
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
        policies = self.get_components_dict('sdk.policies')
        for policy in policies.values():
            for p in policy.values():
                if p.func_name == policy_name:
                    matched_policy = p

                    policy_results = matched_policy.func.execute(*args, **kwargs)
                    
                    return policy_results
