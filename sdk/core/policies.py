from typing import Callable

#! need to make a dataclass for the required output of the policy
#! maybe even a dataclass for the input

class Policies:

    policies = {}
    
    def __init__(self):
      from sdk import policies

    @classmethod
    def register(cls) -> Callable:
        """ 
        """

        def inner_wrapper(wrapped_class: Callable) -> Callable:
            cls.policies[wrapped_class.__name__] = wrapped_class

            return wrapped_class

        return inner_wrapper
    
    def __call__(self, policy, object):
        feched_policy = self.policies[policy]
        policy_results = feched_policy.execute(object)
        
        return policy_results
