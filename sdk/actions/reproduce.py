""" 
Reproduce Action
----------------
This action is used to reproduce two dooders
"""

from sdk.core.action import Action
from sdk.core import Policy
from sdk.core.settings import Settings
from sdk.core import Condition


@Action.register()
def reproduce(dooderX) -> None:
    """
    Apply the reproduction policy to two dooders, create the offspring dooder
    and place it in the simulation.

    The function will first check if the dooder is hungry and if it is old
    enough to reproduce. If the dooder is not hungry and old enough, it will
    find a partner. If a partner is found, the reproduction policy will be
    applied to the two dooders. The offspring will be created and placed in
    the simulation. The offspring will inherit the weights from the parents
    using the internal models.

    Parameters
    ----------
    dooderX : Dooder
        The dooder that is reproducing.

    Examples
    --------
    >>> from sdk.core.action import Action
    >>> from sdk.core.dooder import Dooder
    >>>
    >>> dooder = Dooder()
    >>> Action.execute(dooder, 'reproduce')
    """
    reproduction_policy = Settings.search('Reproduction')

    if dooderX.hunger <= 1 and dooderX.age > 5:
    # if Condition.check_new('reproduction', dooderX):
    #     pass
    # else:
        
        dooderY = dooderX.find_partner()

        if dooderY:
            genetics = Policy.execute(reproduction_policy, dooderX, dooderY)
            offspring = dooderX.simulation.arena._generate_dooder(
                dooderX.position)
            offspring.internal_models.inherit_weights(genetics)
            offspring.simulation.arena.place_dooder(
                offspring, offspring.position)

            offspring.parents = (dooderX.id, dooderY.id)

            dooderX.reproduction_count += 1
            dooderY.reproduction_count += 1

            dooderX.log(granularity=1,
                        message=f"Reproduced with {dooderY.id} and created {offspring.id}",
                        scope='Dooder')

        else:
            dooderX.log(granularity=2, message="No partner found",
                        scope='Reproduction')

    else:
        pass
