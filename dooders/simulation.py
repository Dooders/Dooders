from random import choices

from mesa import Model

from dooders.dooder import Dooder, Energy
from dooders.enviroment import Environment
from dooders.information import Information
from dooders.parameters import ExperimentParameters
from dooders.time import Time


class Simulation(Model):
    """
    """

    def __init__(
            self,
            experiment_id: int,
            params: ExperimentParameters) -> None:
        """
        Primary class to handle the simulation. A simulation will have access to 
        many different components

        Args:
            params: Experiment parameters.
        """
        super().__init__()
        self.params = params
        self.initial_agents = params.agents
        self.initial_energy_value = params.initial_energy_value
        self.initial_energy_count = params.initial_energy_count
        self.width = params.width
        self.height = params.height
        self.verbose = params.verbose
        self.schedule = Time(self)
        self.environment = Environment(self.width, self.height, torus=True)
        self.information = Information(experiment_id, model_reporters={
            "AgentCount": lambda m: m.schedule.get_agent_count()},
            agent_reporters={'EnergyCounts': 'energy', "DirectionCounts": 'direction'})  # need a dataclass here
        self.agent_count = 0

        # Spawn initial agents
        self.spawn_agents(self.initial_agents)
        self.place_energy(self.initial_energy_count)
        self.running = True
        self.information.collect(self)  # log current state before starting

    def spawn_agent(self, x: int, y: int) -> None:
        """
        Spawn a new agent at the given location. 
        Args:
            x: The x-coordinate of the new agent.
            y: The y-coordinate of the new agent.
        """
        dooder = Dooder(self.next_id(), (x, y), self)
        self.environment.place_agent(dooder, (x, y))
        self.schedule.add(dooder)
        self.agent_count += 1

    def spawn_agents(self, agent_count: int) -> None:
        """
        Spawn a number of new agents at random locations.
        Args:
            agent_count: The number of agents to spawn.
        """
        for i in range(agent_count):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.spawn_agent(x, y)

    def _place_energy(self, x: int, y: int) -> None:
        """
        Place an energy at the given location.

        Args:
            x: The x-coordinate of the new energy.
            y: The y-coordinate of the new energy.

        """
        energy = Energy(self.next_id(), (x, y), self)
        self.environment.place_agent(energy, (x, y))

    def place_energy(self, energy_count: int = None) -> None:
        """
        Place a number of energy at random locations.

        Args:
            energy_count: The number of energy to place.
        """
        locations = [(loc[1], loc[2]) for loc in self.environment.coord_iter()]
        random_locations = choices(locations, k=energy_count)
        for x, y in random_locations:
            self._place_energy(x, y)

    def cycle(self) -> None:
        """
        Advance the model by one cycle.        
        """
        self.schedule.step()
        # collect data at the end of the cycle
        self.information.collect(self)

    def run_model(self, step_count: int) -> None:
        """Run the model for a specified number of steps."""
        while self.running and self.schedule.time < step_count:
            self.place_energy(self.initial_energy_count)
            self.agent_count = self.schedule.get_agent_count()
            self.cycle()

    def reset(self) -> None:
        """
        Reinstantiate the model object, using the current parameters.

        This is useful for resetting the model after a parameter change.
        """
        self.__init__(self.params)

    def stop(self) -> None:
        """Stop the model."""
        self.running = False

    def set_parameters(self, params: ExperimentParameters) -> None:
        """
        Manually set the parameters of the model and reset the simulation.

        Args:
            params: The new parameters to use.
        """
        self.params = params
        self.reset()

    def get_results(self) -> dict:
        """Get the step results of the simulation."""
        return self.information.get_result_dict()

    @property
    def results(self):
        return "__test__"
