import math


def get_direction(origin: tuple, destination: tuple) -> str:
    """
    Get the direction from one position to another.

    Args:
        origin: The (x, y) position of the origin
        destination: The (x, y) position of the destination

    Returns:
        The direction from the origin to the destination
     """
    compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    deltaX = destination[0] - origin[0]
    deltaY = destination[1] - origin[1]

    degrees = math.atan2(deltaX, deltaY)/math.pi*180
    if degrees < 0:
        degrees_final = 360 + degrees
    else:
        degrees_final = degrees

    compass_lookup = round(degrees_final / 45)

    return compass_brackets[compass_lookup]
