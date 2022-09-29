from sdk.core.strategy import Strategies

from random import choices
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from sdk.simulation import Simulation

@Strategies.register("Placement")
def random_location(simulation: 'Simulation', number: int) -> list:
    """ 
    Generates a list of locations for the given number of resources and based on the provided strategy.

    Args:
        simulation (Simulation): The simulation object.
        number (int): The number of locations to generate.

    Returns:
        A list of locations.
    """
    locations = [(loc[1], loc[2])
                 for loc in simulation.environment.coord_iter()]
    random_locations = choices(locations, k=number)

    return random_locations