""" 
Energy
-----
Represents energy in the environment. 

Energy is consumed by agents to increase its lifespan.
"""

from typing import TYPE_CHECKING

from sdk.core import Strategy, compile_strategy

if TYPE_CHECKING:
    from sdk.core.data import Position, UniqueID
    from sdk.models.resources import Resources


EnergyStrategy = Strategy.load_strategy('energy')


class Energy:
    """ 
    Energy object used for an agent to continue in the simulation.
    Dooders must consume energy to increase their lifespan.
    
    Parameters
    ----------
    unique_id: UniqueID
        Unique ID of the object.
    position: Position
        Position of the object.
    resources: Resources
        Resources object.
        
    Attributes
    ----------
    unique_id: UniqueID
        See Parameters.
    position: Position
        See Parameters.
    resources: Resources
        See Parameters.
    cycle_count: int
        Current cycle count. AKA, age.
    strategies: dict    
        Defined Energy strategies

    """

    def __init__(self,
                 unique_id: 'UniqueID',
                 position: 'Position',
                 resources: 'Resources') -> None:
        self.unique_id = unique_id
        self.strategies = compile_strategy(self, EnergyStrategy)
        self.position = position
        self.cycle_count = 0
        self.resources = resources

    def step(self) -> None:
        """
        Step through for the object.
        If the object gets to its max age, it will be dissipated.
        """
        self.cycle_count += 1
        if self.cycle_count >= self.EnergyLifespan:
            self.consume('dissipate')
            self.resources.dissipated_energy += 1
            self.resources.log(
                granularity=3, message=f"Energy {self.unique_id} dissipated", scope='Energy')

    def consume(self, type=None) -> None:
        """
        Consume the energy object and remove it from the environment.
        
        Parameters
        ----------
        type: str
            Type of consumption. 
            If None, it will counted as consumed energy.
        """

        self.resources.remove(self)
        self.resources.simulation.environment.remove_object(self)
        if type is None:
            self.resources.consumed_energy += 1

        self.resources.log(
            granularity=3, message=f"Energy {self.unique_id} consumed", scope='Energy')

    @property
    def name(self) -> str:
        """ 
        Returns
        -------
        name: str
            Name of the object
        """
        return self.__class__.__name__
