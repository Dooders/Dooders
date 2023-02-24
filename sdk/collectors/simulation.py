""" 
Simulation collectors
---------------------
Collectors that are not specific to a single object type.
"""

from statistics import mean

from sdk.core.core import Core


@Core.register('collector')
def dooder_count(simulation) -> int:
    """
    The number of dooders in the simulation.

    Parameters
    ----------
    simulation : Simulation
        The simulation to collect data from.

    Returns
    -------
    int
        The number of dooders in the simulation.
    """
    return simulation.time.get_object_count('Dooder')


@Core.register('collector')
def energy_count(simulation) -> int:
    """
    The number of energy in the simulation.

    Parameters
    ----------
    simulation : Simulation
        The simulation to collect data from.

    Returns
    -------
    int
        The number of energy in the simulation.
    """
    return simulation.environment.get_object_count('Energy')


# @Collector.register('DirectionCounts')
# def get_direction_counts(simulation) -> dict:
#     """Return the number of moves in each direction."""
#     dooders = simulation.time.get_objects('Dooder')

#     from collections import Counter
#     direction_list = [dooder.direction for dooder in dooders]
#     direction_counts = Counter(direction_list)

#     return dict(direction_counts)


# @Collector.register('TotalDooderEnergySupply')
# def get_total_energy_supply(simulation) -> int:
#     """ Return the total energy supply of all dooders in the simulation. """
#     energy_supply = [
#         dooder.energy_supply for dooder in simulation.time.get_objects('Dooder')]

#     if len(energy_supply) == 0:
#         return 0

#     return sum(energy_supply)


@Core.register('collector')
def average_energy_age(simulation) -> float:
    """
    Return the average age of energy in the simulation.

    Parameters
    ----------
    simulation : Simulation
        The simulation to collect data from.

    Returns
    -------
    float
        The average age of energy in the simulation.
    """
    energy_age = [
        energy.cycle_count for energy in simulation.environment.get_objects('Energy')]

    if len(energy_age) == 0:
        return 0

    return round(mean(energy_age), 2)

# @Collector.register()
# def average_genetics(simulation) -> dict:
#     """
#     Return the average genetics of all dooders in the simulation.

#     Parameters
#     ----------
#     simulation : Simulation
#         The simulation to collect data from.

#     Returns
#     -------
#     dict
#         The average genetics of all dooders in the simulation.
#     """
#     dooders = simulation.arena.active_dooders

#     genetic_list = []

#     for dooder in dooders.values():
#         genetic_list.append(dooder.genetics)

#     df = pd.DataFrame.from_dict(genetic_list)

#     return dict(df.mean())


# @Collector.register('AverageDooderAge')
# def get_average_energy_age(simulation) -> float:
#     """Return the average age of energy in the simulation."""
#     dooder_age = [
#         dooder.age for dooder in simulation.environment.get_objects('Dooder')]

#     if len(dooder_age) == 0:
#         return 0

#     return round(mean(dooder_age), 2)
