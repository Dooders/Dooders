""" 
Energy
-----
Represents energy in the environment. 

Energy is consumed by agents to increase its lifespan.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dooders.sdk.core.data import Position, UniqueID
    from dooders.sdk.models.resources import Resources


class Energy:
    """ 
    Energy object used for an agent to continue in the simulation.
    Dooders must consume energy to increase their lifespan.

    Parameters
    ----------
    id: UniqueID
        Unique ID of the object.
    position: Position
        Position of the object.
    resources: Resources
        Resources object.

    Attributes
    ----------
    id: UniqueID
        See Parameters.
    position: Position
        See Parameters.
    resources: Resources
        See Parameters.
    age: int
        Current cycle count. AKA, age.
    strategies: dict    
        Defined Energy strategies

    Methods
    -------
    step()
        Step through for the object.
        If the object gets to its max age, it will be dissipated.
    consume(type=None)
        Consume the energy object and remove it from the environment.
    name()
        Returns the name of the object.

    Properties
    ----------
    name: str
        Name of the object
    """

    def __init__(self,
                 id: 'UniqueID',
                 position: 'Position',
                 resources: 'Resources') -> None:
        self.id = id
        self.position = position
        self.age = 0
        self.resources = resources

    def __del__(self):
        self.resources = None

    def step(self) -> None:
        """
        Step through for the object.
        If the object gets to its max age, it will be dissipated.
        """
        self.age += 1
        if self.age >= self.EnergyLifespan():
            self.consume()
            self.resources.dissipated_energy += 1
            self.resources.log(
                granularity=3, message=f"Energy {self.id} dissipated", scope='Energy')

    def consume(self) -> None:
        """
        Consume the energy object and remove it from the environment.

        Parameters
        ----------
        type: str
            Type of consumption. 
            If None, it will counted as consumed energy.
        """

        self.resources.simulation.environment.remove_object(self)
        self.resources.remove(self)

        self.resources.log(
            granularity=3, message=f"Energy {self.id} consumed", scope='Energy')

    @property
    def name(self) -> str:
        """ 
        Returns
        -------
        name: str
            Name of the object
        """
        return self.__class__.__name__
