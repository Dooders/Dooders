from sdk.core.action import Actions
from sdk.utils.get_direction import get_direction


@Actions.register()
def move(dooder):
    policy = dooder.simulation.params.get('Policies').Movement
    destination = dooder.simulation.policies(policy, dooder)

    if destination == dooder.position:
        pass
    else:
        origin = dooder.position
        dooder.direction = get_direction(origin, destination)
        dooder.simulation.environment.move_object(dooder, destination)
        dooder.log(
            granularity=2, message=f"Moved {dooder.direction} from {origin} to {destination}", scope='Dooder')
        dooder.position = destination
