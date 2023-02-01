""" 
Reproduce Action
----------------
This action is used to reproduce two dooders
"""

from sdk.core.action import Action
from sdk.core import Policy


@Action.register()
def reproduce(dooderX) -> None:
    """
    Apply the reproduction policy to two dooders, 
    create the offspring dooder
    and place it in the simulation.

    Parameters
    ----------
    dooderA: Dooder 
        The first Dooder.
    """
    reproduction_policy = dooderX.simulation.params.get('Policies').Reproduction

    #! make this a condition
    if dooderX.hunger == 0 and dooderX.age > 5:

        dooderY = dooderX.find_partner()

        if dooderY:
            genetics = Policy.execute(reproduction_policy, dooderX, dooderY) #! make sure this will execute for all internal_models
            offspring = dooderX.simulation.society._generate_dooder(
                dooderX.position)
            offspring.internal_models.inherit_weights(genetics) #! need a consistent way to inherit all the weights in the internal models
            offspring.simulation.society.place_dooder(
                offspring, offspring.position)
            
            offspring.parents = (dooderX.unique_id, dooderY.unique_id)
            
            dooderX.reproduction_count += 1
            dooderY.reproduction_count += 1

            dooderX.log(granularity=1,
                        message=f"Reproduced with {dooderY.unique_id} and created {offspring.unique_id}",
                        scope='Dooder')

        else:
            dooderX.log(granularity=1, message="No partner found",
                        scope='Reproduction')

    else:
        pass
