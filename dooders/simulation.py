from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa import Model
from dooders.agent import Dooder


class Simulation(Model):
    """
    """

    height = 20
    width = 20

    initial_agents = 10
    verbose = True  # Print-monitoring

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        width=20,
        height=20,
        initial_agents=initial_agents,
        verbose=verbose
    ):
        """
        """
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.initial_agents = initial_agents
        self.verbose = verbose

        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, torus=True)
        self.datacollector = DataCollector(
            {"Dooders": lambda m: m.schedule.get_agent_count()})
        self.agent_count = 0

        # Create agents:
        for i in range(self.initial_agents):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            happiness = self.random.randrange(10, 90)
            dooder = Dooder(self.next_id(), (x, y), self)
            self.grid.place_agent(dooder, (x, y))
            self.schedule.add(dooder)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time, self.schedule.get_agent_count()])

    def run_model(self, step_count=10):

        if self.verbose:
            print("Initial number dooders: ", self.schedule.get_agent_count())

        for i in range(step_count):
            self.agent_count = self.schedule.get_agent_count()
            # running status
            # metrics
            self.step()

        if self.verbose:
            print("")
            print("Final number dooders: ", self.schedule.get_agent_count())
