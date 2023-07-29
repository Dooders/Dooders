""" 
Reproduce Action
----------------
This action is used to reproduce two dooders
"""

from dooders.sdk.core import Policy
from dooders.sdk.core.condition import Condition
from dooders.sdk.core.core import Core
from dooders.sdk.core.settings import Settings


@Core.register('action')
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

    result, reason = Condition.check('reproduction', dooderX)

    if result:

        dooderY = dooderX.find_partner()

        if dooderY:
            genetics = Policy.execute(reproduction_policy, dooderX, dooderY)
            offspring = dooderX.simulation.arena._generate_dooder(
                dooderX.position, tag='Offspring')
            offspring.internal_models.inherit_weights(genetics)
            offspring.get_gene_embedding()
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
        message_reason = f"Reproduction failed: {reason}"
        dooderX.log(granularity=2, message=message_reason,
                    scope='Reproduction')
