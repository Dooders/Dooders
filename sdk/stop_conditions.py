from typing import Callable


class ConditionRegistry:
    """ The factory class for creating executors"""

    registry = {}
    """ Internal registry for available executors """

    @classmethod
    def register_condition(cls, name: str) -> Callable:
        """ 
        """

        def inner_wrapper(wrapped_class: Callable) -> Callable:
            cls.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def check_conditions(cls, simulation):
        """ 
        """

        for condition in cls.registry:
            func = cls.registry[condition]
            if func(simulation):
                return True, condition
        return False, None


@ConditionRegistry.register_condition('check_max_cycle')
def check_max_cycle(simulation):
    if simulation.cycles >= simulation.params.Simulation.MaxCycles:
        return True


@ConditionRegistry.register_condition('check_simulation_running')
def check_simulation_running(simulation):
    if not simulation.running:
        return True


@ConditionRegistry.register_condition('check_dooder_count')
def check_dooder_count(simulation):
    if len(simulation.environment.get_objects("Dooder")) == 0:
        return True
