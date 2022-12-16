import copy
from sdk.core.actions import Actions


@Actions.register()
def reproduce(dooderA):
    """
    Apply the reproduction policy to two dooders, create the offspring dooder
    and place it in the simulation.

    Args:
        dooderA (Dooder): The first Dooder.
    """
    from sdk.core import Policies
    reproduction_policy = Policies.policies['AverageWeights']

    if dooderA.hunger == 0 and dooderA.age > 5:

        dooderB = dooderA.find_partner()

        if dooderB:
            genetics = reproduction_policy.execute(dooderA, dooderB) #! make sure this will execute for all internal_models
            offspring = dooderA.simulation.society._generate_dooder(
                dooderA.position)
            offspring.internal_models.inherit_weights(genetics) #! need a consistent way to inherit all the weights in the internal models
            offspring.simulation.society.place_dooder(
                offspring, offspring.position)

            dooderA.log(granularity=1,
                        message=f"Reproduced with {dooderB.unique_id} and created {offspring.unique_id}",
                        scope='Dooder')

        else:
            dooderA.log(granularity=1, message="No partner found",
                        scope='Reproduction')

    else:
        pass
