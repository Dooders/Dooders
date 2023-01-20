""" 
Reproduce Action
----------------
This action is used to reproduce two dooders
"""

from sdk.core.action import Actions


@Actions.register()
def reproduce(dooderA) -> None:
    """
    Apply the reproduction policy to two dooders, create the offspring dooder
    and place it in the simulation.

    Parameters
    ----------
    dooderA: Dooder 
        The first Dooder.
    """
    reproduction_policy = dooderA.simulation.params.get('Policies').Reproduction

    if dooderA.hunger == 0 and dooderA.age > 5:

        dooderB = dooderA.find_partner()

        if dooderB:
            genetics = dooderA.simulation.policies(reproduction_policy, dooderA, dooderB) #! make sure this will execute for all internal_models
            offspring = dooderA.simulation.society._generate_dooder(
                dooderA.position)
            offspring.internal_models.inherit_weights(genetics) #! need a consistent way to inherit all the weights in the internal models
            offspring.simulation.society.place_dooder(
                offspring, offspring.position)
            
            offspring.parents = (dooderA.unique_id, dooderB.unique_id)
            
            dooderA.reproduction_count += 1
            dooderB.reproduction_count += 1

            dooderA.log(granularity=1,
                        message=f"Reproduced with {dooderB.unique_id} and created {offspring.unique_id}",
                        scope='Dooder')

        else:
            dooderA.log(granularity=1, message="No partner found",
                        scope='Reproduction')

    else:
        pass
