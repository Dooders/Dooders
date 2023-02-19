""" 
Environment Collectors
----------------------
Collectors that collect information about the environment.
"""

from sdk.core.collector import Collector


@Collector.register()
def space_contents_count(simulation) -> dict:
    """ 
    The number of contents in each Space.

    Parameters
    ----------
    simulation : Simulation
        The simulation to check

    Returns
    -------
    Space: dict
        A dictionary with the number of contents in each Space.

    Sample Output
    ------------
    Coordinate: Contents count
    {
        (0, 0): 0,
        (0, 1): 0,
        (0, 2): 0,
        (0, 3): 0
    }
    """

    space_contents = {}

    for space in simulation.environment.spaces():
        space_contents[space.coordinates] = len(space.contents)

    return space_contents


@Collector.register()
def state_space_pattern(simulation) -> dict:
    """ 
    Contents pattern for each Space.

    The pattern is a list of integers representing each possible content state.

    The first integer is the number of contents in the Space that is a dooder object.
    The second integer is the number of contents in the Space that is an energy object.    

    So a total of 2 dooders and 1 energy would be 21.
    And, a total of 1 dooder and 2 energy would be 12.

    Parameters
    ----------
    simulation : Simulation
        The simulation to check

    Returns
    -------
    Space: dict
        A dictionary with the contents pattern for each Space.

    Sample Output
    ------------
    Coordinate: Contents Pattern 
    {
        (0, 0): 20,
        (0, 1): 01,
        (0, 2): 11,
        (0, 3): 43 
    }
    """
    space_contents = {}

    for space in simulation.environment.spaces():
        pattern = space.contents_pattern
        space_contents[space.coordinates] = pattern

    return space_contents
