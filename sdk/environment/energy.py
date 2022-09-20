from typing import TYPE_CHECKING

from sdk.strategies.strategies import Strategies, compile_strategy

if TYPE_CHECKING:
    from sdk.environment.resources import Resources


EnergyStrategy = Strategies.load_strategy('sdk/environment/energy.yml')


class Energy:
    """ 
    
    """
    
    def __init__(self, unique_id: str, position: tuple, resources: 'Resources') -> None:
        """ 
        Args:
            unique_id: Unique ID of the object.
            position: Position of the object.
            
        Attributes:
            unique_id: Unique ID of the object.
            position: Position of the object.
            resources: Resources object
            cycle_count (int): Current cycle count
        """
        self.unique_id = unique_id
        self.strategies = compile_strategy(self, EnergyStrategy)
        self.position = position
        self.cycle_count = 0
        self.resources = resources
        
    def step(self) -> None:
        """
        """
        self.cycle_count += 1
        if self.cycle_count >= self.Lifespan:
            self.consume()
            self.resources.log(
                granularity=3, message=f"Energy {self.unique_id} dissipated", scope='Energy')

    def consume(self) -> None:
        """
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
