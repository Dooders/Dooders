from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from dooders.agents import Dooder


class Simulation(Model):
    """
    Wolf-Sheep Predation Model
    """

    height = 20
    width = 20

    initial_agents = 100
    verbose = False  # Print-monitoring

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        width=20,
        height=20,
        initial_agents=100
    ):
        """
        """
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.initial_agents = initial_agents

        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, torus=True)
        self.datacollector = DataCollector({"Dooders": lambda m: m.schedule.get_agent_count()})

        # Create agents:
        for i in range(self.initial_agents):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            happiness = self.random.randrange(10,90)
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
            print([self.schedule.time, self.schedule.get_type_count(Dooder)])

    def run_model(self, step_count=200):

        if self.verbose:
            print("Initial number dooders: ", self.schedule.get_type_count(Dooder))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print("Final number dooders: ", self.schedule.get_type_count(Dooder))