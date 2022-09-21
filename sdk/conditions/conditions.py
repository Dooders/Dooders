from typing import Callable

#! might need to have ability for and/or condition combinations
#! check returns true/false and the probability to check, if needed (ask fate)


class Conditions:
    """ 
    The factory class to be used as a decorator to register a stop condition. 
    """

    # Internal registry for available conditions.
    registry = {}

    @classmethod
    def register(cls, name: str) -> Callable:
        """ 
        Register a stop condition.

        Args:
            name: The name of the stop condition.

        Returns:
            The decorator function.
        """

        def inner_wrapper(wrapped_class: Callable) -> Callable:
            purpose = cls.infer_purpose(cls, wrapped_class)
            if purpose not in cls.registry:
                cls.registry[purpose] = {}
            cls.registry[purpose][name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    def infer_purpose(self, condition: Callable) -> str:
        """ 
        Infer the purpose based on the filename

        """
        return condition.__module__.split('.')[-1]

    def get_purpose(self, condition):
        for purpose in self.registry:
            if condition in self.registry[purpose]:
                return purpose
        return None

    @classmethod
    def check_conditions(cls, purpose, *args, **kwargs):
        """ 
        Check if any of the registered conditions are met.

        Args:
            simulation: The simulation to check the conditions for.

        Returns:
            True if any of the conditions are met.
        """
        # check in registry in each purpose to see what purpose is the condition from

        for condition in cls.registry[purpose]:
            func = cls.registry[purpose][condition]
            if func(*args, **kwargs):
                return True, condition
        return False, None
