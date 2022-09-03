from statistics import mean
from typing import Callable


class CollectorRegistry:
    """ 
    The factory class for creating executors
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

@CollectorRegistry.register_collector('DooderCount', 'Simulation')
def get_dooder_count(simulation) -> int:
    """Return the number of dooders in the simulation."""
    return simulation.time.get_object_count('Dooder')

@CollectorRegistry.register_collector('EnergyCount', 'Simulation')
def get_energy_count(simulation) -> int:
    """Return the number of energy in the simulation."""
    return simulation.time.get_object_count('Energy')

@CollectorRegistry.register_collector('DirectionCounts', 'Simulation')
def get_direction_counts(simulation) -> dict:
    """Return the number of moves in each direction."""
    dooders = simulation.time.get_objects('Dooder')

    from collections import Counter
    direction_list = [dooder.direction for dooder in dooders]
    direction_counts = Counter(direction_list)

    return dict(direction_counts)

@CollectorRegistry.register_collector('TotalDooderEnergySupply', 'Simulation')
def get_total_energy_supply(simulation) -> int:
    """ Return the total energy supply of all dooders in the simulation. """
    energy_supply = [
        dooder.energy for dooder in simulation.time.get_objects('Dooder')]

    if len(energy_supply) == 0:
        return 0

    return sum(energy_supply)

@CollectorRegistry.register_collector('AverageEnergyAge', 'Simulation')
def get_average_energy_age(simulation) -> float:
    """Return the average age of energy in the simulation."""
    energy_age = [
        energy.cycle_count for energy in simulation.time.get_objects('Energy')]

    if len(energy_age) == 0:
        return 0

    return round(mean(energy_age), 2)

@CollectorRegistry.register_collector('AverageBehaviorProfile', 'PostCollect')
def get_average_behavior_profile(simulation) -> dict:
    pass
