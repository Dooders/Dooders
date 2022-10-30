




class Policies:

    policies = {}
    
    def __init__(self):
      # import all the policies from policy fooder
      pass

    @classmethod
    def register(cls) -> Callable:
        """ 
        """

        def inner_wrapper(wrapped_class: Callable) -> Callable:
            cls.policies[wrapped_class.__name__] = wrapped_class

            return wrapped_class

        return inner_wrapper
    
    def __call__(self, policy_type, policy, object):
        feched_policy = self.policies[policy_type][policy]
        policy_results = feched_policy.execute(object)
        
        return policy_results
