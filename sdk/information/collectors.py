""" 
The CollectorRegistry is a global registry of collectors. A new collector
is added through the register_collector() decorator. 

The decorator takes the name of the collector and component as arguments. The
component indicates what component or module the collector belongs to. The 
collector name is used to identify the collector in the output.

A collector serves as a method to extract information from the simulation 
at the end of each cycle. The information is stored in a dictionary, which 
is then passed to the Information component.

A collector can return any type of information. Every Collector must input 
'simulation' as an argument. The simulation object is used to extract 
information from the simulation.
"""

from functools import partial
from statistics import mean
from typing import Callable

from sdk.base.base_information import BaseCollector


class Collectors:
    """ 
    The factory class for creating collectors

    The CollectorRegistry is a global registry of collectors. A new collector
    is added through the register_collector() decorator.
    """

    # The registry of collectors
    registry = []

    @classmethod
    def register_collector(cls, name: str, component: str) -> Callable:
        """ 
        Register a collector in the registry.

        Args:
            name: Name of the collector.
            component: Component of the collector.

        Returns:
            The decorator function.
        """

        def inner_wrapper(wrapped_class: Callable) -> Callable:
            cls.registry.append(
                {'name': name, 'function': wrapped_class, 'component': component})
            return wrapped_class

        return inner_wrapper
    
    @classmethod
    def compile_collectors(cls, Information):
        for collector in cls.registry:
            collector = BaseCollector(**collector)
            component = collector.component

            if component not in Information.collectors:
                Information.collectors[component] = {}
                Information.data[component] = {}

            if type(collector.function) is str:
                func = partial(Information._getattr, collector.function)
            else:
                func = collector.function

            Information.collectors[component][collector.name] = func
            Information.data[component][collector.name] = []
            
    @classmethod
    def run_collectors(cls, Information, simulation):
        for component in Information.collectors:
            cls._collect(Information, component, simulation)
            
    def _collect(self, Information, component: str, simulation) -> None:
        """
        Run all the collectors for the given component.

        Args:
            Information: Information object to collect data from.
            component: Component to collect data from.
            simulation: Simulation object to collect data from.
        """
        for name, func in Information.collectors[component].items():

            if callable(func):
                Information.data[component][name].append(func(simulation))
            else:

                if func[1] is None:
                    Information.data[component][name].append(func[0](simulation))
                else:
                    Information.data[component][name].append(
                        func[0](simulation, **func[1]))



# ===========================
# Base Collectors
# ===========================

@Collectors.register_collector('DooderCount', 'Simulation')
def get_dooder_count(simulation) -> int:
    """Return the number of dooders in the simulation."""
    return simulation.time.get_object_count('Dooder')


@Collectors.register_collector('EnergyCount', 'Simulation')
def get_energy_count(simulation) -> int:
    """Return the number of energy in the simulation."""
    return simulation.environment.get_object_count('Energy')


@Collectors.register_collector('DirectionCounts', 'Simulation')
def get_direction_counts(simulation) -> dict:
    """Return the number of moves in each direction."""
    dooders = simulation.time.get_objects('Dooder')

    from collections import Counter
    direction_list = [dooder.direction for dooder in dooders]
    direction_counts = Counter(direction_list)

    return dict(direction_counts)


@Collectors.register_collector('TotalDooderEnergySupply', 'Simulation')
def get_total_energy_supply(simulation) -> int:
    """ Return the total energy supply of all dooders in the simulation. """
    energy_supply = [
        dooder.energy_supply for dooder in simulation.time.get_objects('Dooder')]

    if len(energy_supply) == 0:
        return 0

    return sum(energy_supply)


@Collectors.register_collector('AverageEnergyAge', 'Simulation')
def get_average_energy_age(simulation) -> float:
    """Return the average age of energy in the simulation."""
    energy_age = [
        energy.cycle_count for energy in simulation.environment.get_objects('Energy')]

    if len(energy_age) == 0:
        return 0

    return round(mean(energy_age), 2)


@Collectors.register_collector('AverageBehaviorProfile', 'PostCollect')
def get_average_behavior_profile(simulation) -> dict:
    pass
