from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa import Model
from dooders.agent import Dooder
from dooders.parameters import Parameters


class Simulation(Model):
    """
    
    """

    def __init__(
        self,
        params: Parameters,
    ):
        """
        """
        super().__init__()
        self.params = params
        self.agent_count = params.initial_agents
        self.width = params.width
        self.height = params.height
        self.verbose = params.verbose
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, torus=True)
        self.datacollector = DataCollector(
            {"Dooders": lambda m: m.schedule.get_agent_count()})
        self.agent_count = 0

        # Spawn initial agents
        self.spawn_agents(self.initial_agents)
        self.running = True
        self.datacollector.collect(self)

    def spawn_agent(self, x, y):
        """Spawn a new agent at the given location."""
        dooder = Dooder(self.next_id(), (x, y), self)
        self.grid.place_agent(dooder, (x, y))
        self.schedule.add(dooder)
        self.agent_count += 1

    def spawn_agents(self, count):
        """Spawn a number of new agents at random locations."""
        for i in range(count):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.spawn_agent(x, y)

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time, self.schedule.get_agent_count()])

    def run_model(self, step_count=10):
        """Run the model for a specified number of steps."""
        while self.running and self.schedule.time < step_count:
            self.agent_count = self.schedule.get_agent_count()
            self.step()

    def reset(self):
        """Reinstantiate the model object, using the current parameters."""
        self.__init__(
            width=self.width,
            height=self.height,
            initial_agents=self.initial_agents,
            verbose=self.verbose
        )

    def stop(self):
        """Stop the model."""
        self.running = False
