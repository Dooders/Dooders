
import copy


def reproduce(dooderA):
    """
    Apply the reproduction policy to two dooders, create the offspring dooder
    and place it in the simulation.

    """
    from sdk.core import Policies
    reproduction_policy = Policies.policies['AverageWeights']
    dooderB = dooderA.find_partner()

    if dooderB:
        genetics = reproduction_policy.execute(dooderA, dooderB)
        offspring = dooderA.simulation.society._generate_dooder(
            dooderA.position)
        offspring.movement = copy.deepcopy(dooderA.movement) #! this doesn't work
        offspring.movement.inherit_weights(genetics)
        offspring.simulation.society.place_dooder(
            offspring, offspring.position)

        offspring.log(granularity=1,
                      message=f"Created {offspring.unique_id}",
                      scope='Dooder')

        dooderA.log(granularity=1,
                    message=f"Reproduced with {dooderB.unique_id} and created {offspring.unique_id}",
                    scope='Dooder')

    else:
        dooderA.log(granularity=1, message="No partner found",
                    scope='Reproduction')
