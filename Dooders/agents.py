from dooders.random_walk import RandomWalker

class Dooder(RandomWalker):
    """
    """
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, pos, model)

    
    def kill(self, agent):
        self.model.grid.remove_agent(agent)
        self.model.schedule.remove(agent)

    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

    def step(self):
        # move --> action
        self.random_move()





