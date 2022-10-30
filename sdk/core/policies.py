from typing import Callable


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
