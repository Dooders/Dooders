from sdk.core.collector import Collector


@Collector.register('LocationContentsCount')
def location_contents_count(simulation) -> dict:
    """ 
    Returns a dictionary of the number of contents in each location.

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
