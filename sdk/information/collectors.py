from typing import Callable
from pydantic import BaseModel, Field


class CollectorRegistry:
    """ The factory class for creating executors"""

    registry = []
    """ Internal registry for available executors """

    @classmethod
    def register_collector(cls, name: str, component: str) -> Callable:
        """ 
        """

        def inner_wrapper(wrapped_class: Callable) -> Callable:
            cls.registry.append({'name': name, 'function': wrapped_class, 'component': component})
            return wrapped_class

        return inner_wrapper



@CollectorRegistry.register_collector('DooderCount', 'Simulation')
def get_dooder_count(simulation):
    return simulation.time.get_object_count('Dooder')

@CollectorRegistry.register_collector('EnergyCount', 'Simulation')
def get_energy_count(simulation):
    return simulation.time.get_object_count('Energy')

@CollectorRegistry.register_collector('DirectionCounts', 'Simulation')
def get_direction_counts(simulation):
    dooders = simulation.time.get_objects('Dooder')
    
    from collections import Counter
    direction_list = [dooder.direction for dooder in dooders]
    direction_counts = Counter(direction_list)

    return dict(direction_counts)