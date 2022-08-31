from random import choices

from sdk.base import BaseSimulation
from sdk.dooder import Dooder
from sdk.environment import Energy
from sdk.config import ExperimentParameters


class Simulation(BaseSimulation):
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
        super().__init__(experiment_id, params)
        
        self.cycles: int = 0


    def setup(self) -> None:
        """
        Setup the simulation.
        """
        self.spawn_objects(Dooder, self.params.Dooder.StartingAgentCount)
        self.spawn_objects(Energy, self.params.Energy.StartingEnergyCount)

        self.running = True
        self.information.collect(self)

    def spawn_object(self, x: int, y: int, Object) -> None:
        object_name = Object.__name__
        object = Object(self.generate_id(), (x, y), self, self.params.get(object_name))
        self.environment.place_object(object, (x, y))
        self.time.add(object)

    def spawn_objects(self, Object, object_count: int) -> None:
        """
        Spawn a number of new objects at random locations.
        Args:
            object_count: The number of objects to spawn.
        """
        locations = [(loc[1], loc[2]) for loc in self.environment.coord_iter()]
        random_locations = choices(locations, k=object_count)

        for x, y in random_locations:
            self.spawn_object(x, y, Object)

    def cycle(self) -> None:
        """
        Advance the simulation by one cycle.        
        """
        # place new energy
        self.spawn_objects(Energy, self.params.Simulation.CycleEnergyAdd)

        # advance every agent by a step
        self.time.step()

        # collect data at the end of the cycle
        self.information.collect(self)
        
        self.cycles += 1

    def run_simulation(self) -> None:
        """Run the simulation for a specified number of steps."""
        self.setup()

        # todo: Dynamic checks for when to stop simulation
        while self.running and self.time.time < self.params.Simulation.MaxCycles:
            self.cycle()

    def reset(self) -> None:
        """
        Reinstantiate the simulation object, using the current parameters.

        This is useful for resetting the simulation after a parameter change.
        """
        self.__init__(self.experiment_id, self.params)

    def stop(self) -> None:
        """Stop the simulation."""
        self.running = False

    def set_parameters(self, params: ExperimentParameters) -> None:
        """
        Manually set the parameters of the simulation and reset the simulation.

        Args:
            params: The new parameters to use.
        """
        self.params = params
        self.reset()

    def get_results(self) -> dict:
        """Get the step results of the simulation."""
        return self.information.get_result_dict(self)

    def generate_id(self) -> int:
        """Generate a new id for an object."""
        return self.seed.uuid()
    
    def stop_condition(self) -> bool:
        """
        Check if the simulation should stop.
        """
        pass

    @property
    def results(self):
        return "__test__"
