class Energy:
    """ 
    
    """
    
    def __init__(self, unique_id: str, lifespan, position, resources) -> None:
        """ 
        Args:
            unique_id: Unique ID of the object.
            lifespan: Lifespan of the object.
            position: Position of the object.
            
        Attributes:
            unique_id: Unique ID of the object.
            position: Position of the object..
            life_span: The life span of the energy.
            cycle_count: The cycle count of the energy.
        """
        self.unique_id = unique_id
        self.life_span = lifespan
        self.position = position
        self.cycle_count = 0
        self.resources = resources
        
    def step(self) -> None:
        """
        """
        self.cycle_count += 1
        if self.cycle_count >= self.life_span:
            self.resources.consume(self)
            self.resources.log(
                granularity=3, message=f"Energy {self.unique_id} dissipated", scope='Energy')

    def consume(self):
        """
        """
        self.resources.consume(self)
        self.resources.log(
                granularity=3, message=f"Energy {self.unique_id} consumed", scope='Energy')
