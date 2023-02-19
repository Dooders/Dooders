""" 
Reproduce Action
----------------
This action is used to reproduce two dooders
"""

from sdk.core.action import Action
from sdk.core import Policy
from sdk.core.settings import Settings


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
    reproduction_policy = Settings.get('variables')['policies']['Reproduction'].args['value'] #! make this a lot simpler and cleaner

    #! make this a condition
    if dooderX.hunger == 0 and dooderX.age > 5:

        dooderY = dooderX.find_partner()

        if dooderY:
            genetics = Policy.execute(reproduction_policy, dooderX, dooderY) #! make sure this will execute for all internal_models
            offspring = dooderX.simulation.arena._generate_dooder(
                dooderX.position)
            offspring.internal_models.inherit_weights(genetics) #! need a consistent way to inherit all the weights in the internal models
            offspring.simulation.arena.place_dooder(
                offspring, offspring.position)
            
            offspring.parents = (dooderX.id, dooderY.id)
            
            dooderX.reproduction_count += 1
            dooderY.reproduction_count += 1

            dooderX.log(granularity=1,
                        message=f"Reproduced with {dooderY.id} and created {offspring.id}",
                        scope='Dooder')

        else:
            dooderX.log(granularity=1, message="No partner found",
                        scope='Reproduction')

    else:
        pass
