""" 

"""

from typing import TYPE_CHECKING

from sdk.core import Strategy, compile_strategy

if TYPE_CHECKING:
    from sdk.core.data import Position, UniqueID
    from sdk.models.resources import Resources


EnergyStrategy = Strategy.load_strategy('energy')


class Energy:
    """ 

    """

    def __init__(self,
                 unique_id: 'UniqueID',
                 position: 'Position',
                 resources: 'Resources') -> None:
        """ 
        Args:
            unique_id: Unique ID of the object.
            position: Position of the object.
            resources: Resources object.

        Attributes:
            unique_id: See Args.
            position: See Args.
            resources: See Args.
            cycle_count: Current cycle count. AKA, age.
            strategies: Defined Energy strategies
        """
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
        if self.cycle_count >= self.Lifespan:
            self.consume('dissipate')
            self.resources.total_dissipated_energy += 1
            self.resources.log(
                granularity=3, message=f"Energy {self.unique_id} dissipated", scope='Energy')

    def consume(self, type=None) -> None:
        """
        Consume the energy object and remove it from the environment.
        """

        self.resources.remove(self)
        self.resources.simulation.environment.remove_object(self)
        if type is None:
            self.resources.total_consumed_energy += 1

        self.resources.log(
            granularity=3, message=f"Energy {self.unique_id} consumed", scope='Energy')

    @property
    def name(self) -> str:
        """ 
        Returns:
            Name of the object
        """
        return self.__class__.__name__
