import random

from sdk.base_object import BaseObject


class Energy(BaseObject):
    """ 
    
    """
    
    def __init__(self, unique_id: str, position: float, simulation, params: dict) -> None:
        """ 
        Args:
            unique_id: Unique ID of the object.
            position: Position of the object.
            simulation: The simulation object.
            params: The parameters of the simulation.
            
        Attributes:
            unique_id: Unique ID of the object.
            position: Position of the object.
            simulation: The simulation object.
            params: The parameters of the simulation.
            life_span: The life span of the energy.
            cycle_count: The cycle count of the energy.
        """
        super().__init__(unique_id, position, simulation)
        self.params = params
        self.life_span = random.randint(2, self.params.MaxLifespan)
        self.cycle_count = 0
        
    def step(self) -> None:
        """
        """
        self.cycle_count += 1
        if self.cycle_count >= self.life_span:
            self.simulation.environment.remove_object(self)
            self.simulation.time.remove(self)
            self.log(
                granularity=3, message=f"Energy {self.unique_id} dissapated", scope='Energy')

    def consume(self):
        """
        """
        self.simulation.environment.remove_object(self)
        self.simulation.time.remove(self)
