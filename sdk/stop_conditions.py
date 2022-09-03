from typing import Callable


class ConditionRegistry:
    """ 
    The factory class to be used as a decorator to register a stop condition. 
    """

    # Internal registry for available conditions.
    registry = {}

    @classmethod
    def register_condition(cls, name: str) -> Callable:
        """ 
        Register a stop condition.

        Args:
            name: The name of the stop condition.

        Returns:
            The decorator function.
        """

        def inner_wrapper(wrapped_class: Callable) -> Callable:
            cls.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def check_conditions(cls, simulation) -> bool:
        """ 
        Check if any of the registered conditions are met.

        Args:
            simulation: The simulation to check the conditions for.

        Returns:
            True if any of the conditions are met.
        """

        for condition in cls.registry:
            func = cls.registry[condition]
            if func(simulation):
                return True, condition
        return False, None


@ConditionRegistry.register_condition('check_max_cycle')
def check_max_cycle(simulation) -> bool:
    """ 
    Check if the maximum number of cycles has been reached.
    """
    if simulation.cycles >= simulation.params.Simulation.MaxCycles:
        return True


@ConditionRegistry.register_condition('check_simulation_running')
def check_simulation_running(simulation) -> bool:
    """ 
    Check if the simulation is still running.
    """
    if not simulation.running:
        return True


@ConditionRegistry.register_condition('check_dooder_count')
def check_dooder_count(simulation) -> bool:
    """ 
    Check if the number of dooders has reached zero.
    """
    if len(simulation.environment.get_objects("Dooder")) == 0:
        return True
