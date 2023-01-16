from sdk.core.collector import Collector


@Collector.register('LocationContentsCount')
def location_contents_count(simulation) -> dict:
    """ 
    The number of contents in each location.
    
    Returns
    -------
    location_contents: dict
        A dictionary with the number of contents in each location.

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

    location_contents = {}

    for row in simulation.environment.grid:
        for location in row:
            location_contents[location.coordinates] = len(location.contents)

    return location_contents

@Collector.register('StateLocationPattern')
def state_location_pattern(simulation) -> dict:
    """ 
    Contents pattern for each location.
    
    The pattern is a list of integers representing each possible content state.
    
    The first integer is the number of contents in the location that is a dooder object.
    The second integer is the number of contents in the location that is an energy object.    

    So a total of 2 dooders and 1 energy would be 21.
    And, a total of 1 dooder and 2 energy would be 12.
    
    Returns
    -------
    location_contents: dict
        A dictionary with the contents pattern for each location.
    
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
    location_contents = {}

    for row in simulation.environment.grid:
        for location in row:
            pattern = location.contents_pattern
            location_contents[location.coordinates] = pattern

    return location_contents
