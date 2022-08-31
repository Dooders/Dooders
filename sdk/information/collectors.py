from typing import Callable
from pydantic import BaseModel, Field

def get_dooder_count(simulation):
    return simulation.time.get_object_count('Dooder')

def get_energy_count(simulation):
    return simulation.time.get_object_count('Energy')

def get_direction_counts(simulation):
    dooders = simulation.time.get_objects('Dooder')
    
    from collections import Counter
    direction_list = [dooder.direction for dooder in dooders]
    direction_counts = Counter(direction_list)

    return dict(direction_counts)





DEFAULT_COLLECTORS = [
    {'name': "DooderCount", 'function': get_dooder_count, 'component': "Simulation"},
    {'name': "EnergyCount", 'function': get_energy_count, 'component': "Simulation"},
    {'name': "DirectionCounts", 'function': get_direction_counts, 'component': "Simulation"},
]
