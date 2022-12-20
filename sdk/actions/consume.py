from sdk.core.action import Actions
from sdk.models.energy import Energy


@Actions.register()
def consume(dooder):
    """ 
    Consume energy from the environment
    """

    cell_contents = dooder.simulation.environment.get_cell_list_contents(
        dooder.position)
    energy = [obj for obj in cell_contents if isinstance(obj, Energy)]

    if energy:
        food = energy[0]
        food.consume()
        if dooder.hunger > 0:
            dooder.hunger = 0
            
        dooder.energy_consumed += 1

        dooder.log(
            granularity=2, message=f"Consumed energy: {food.unique_id}", scope='Dooder')
    else:
        dooder.hunger += 1
