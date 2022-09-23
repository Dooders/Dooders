""" 

"""

from typing import TYPE_CHECKING

from sdk.strategies.strategies import Strategies, compile_strategy

if TYPE_CHECKING:
    from sdk.data import Position, UniqueID
    from sdk.environment.resources import Resources


EnergyStrategy = Strategies.load_strategy('sdk/environment/energy.yml')


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
            self.consume()
            self.resources.log(
                granularity=3, message=f"Energy {self.unique_id} dissipated", scope='Energy')

    def consume(self) -> None:
        """
        Consume the energy object and remove it from the environment.
        """
    
        self.resources.remove(self)
        self.resources.simulation.environment.remove_object(self)
        self.resources.log(
                granularity=3, message=f"Energy {self.unique_id} consumed", scope='Energy')

    @property
    def name(self) -> str:
        """ 
        Returns:
            Name of the object
        """
        return self.__class__.__name__
