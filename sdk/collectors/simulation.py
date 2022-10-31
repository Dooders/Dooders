from statistics import mean

from sdk.core.collector import Collector


@Collector.register('DooderCount')
def get_dooder_count(simulation) -> int:
    """Return the number of dooders in the simulation."""
    return simulation.time.get_object_count('Dooder')


@Collector.register('EnergyCount')
def get_energy_count(simulation) -> int:
    """Return the number of energy in the simulation."""
    return simulation.environment.get_object_count('Energy')


# @Collector.register('DirectionCounts')
# def get_direction_counts(simulation) -> dict:
#     """Return the number of moves in each direction."""
#     dooders = simulation.time.get_objects('Dooder')

#     from collections import Counter
#     direction_list = [dooder.direction for dooder in dooders]
#     direction_counts = Counter(direction_list)

#     return dict(direction_counts)


@Collector.register('TotalDooderEnergySupply')
def get_total_energy_supply(simulation) -> int:
    """ Return the total energy supply of all dooders in the simulation. """
    energy_supply = [
        dooder.energy_supply for dooder in simulation.time.get_objects('Dooder')]

    if len(energy_supply) == 0:
        return 0

    return sum(energy_supply)


@Collector.register('AverageEnergyAge')
def get_average_energy_age(simulation) -> float:
    """Return the average age of energy in the simulation."""
    energy_age = [
        energy.cycle_count for energy in simulation.environment.get_objects('Energy')]

    if len(energy_age) == 0:
        return 0

    return round(mean(energy_age), 2)
