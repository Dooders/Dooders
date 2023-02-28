""" 
Core: Policies
--------------
This module contains the Policies class,
which is used to register and execute policies.
"""

from typing import Callable

from dooders.sdk.core.core import Core


class Policy(Core):
    """ 
    The factory class to be used as a decorator to register a policy.

    Methods
    -------
    execute(policy_name: str, *args, **kwargs) -> Callable
        Executes a registered policy.
    """

    @classmethod
    def execute(self, policy_name: str, *args, **kwargs) -> Callable:
        """ 
        Executes a registered policy.

        Parameters
        ----------
        policy_name : str, (move, consume, etc.)
            The name of the policy to execute.

        Returns
        -------
        Callable
            The policy that was requested.

        Examples
        --------
        >>> from sdk.core.policy import Policy
        >>>
        >>> Policy.execute('move', agent, environment)
        """
        policies = self.get_components('policy')

        for policy in policies.values():
            for p in policy.values():
                if p.function_name == policy_name:
                    matched_policy = p
                    policy_results = matched_policy.function.execute(
                        *args, **kwargs)
                    return policy_results
