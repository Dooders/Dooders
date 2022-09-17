""" 
Simulation
----------

The simulation class is the main class of the simulation. It is responsible for
initializing the simulation, running the simulation, and displaying the results.
"""

from random import choices

from sdk.base.base_simulation import BaseSimulation
from sdk.config import ExperimentParameters
from sdk.dooder import Dooder
from sdk.dooder.society import Society
from sdk.stop_conditions import ConditionRegistry
from sdk.environment.resources import Resources


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
            experiment_id: The id of the experiment this simulation is a part of.
            params: Experiment parameters.
        
        Attributes:
            cycles: The number of cycles that have passed.
        """
        super().__init__(experiment_id, params)
        
        self.resources = Resources(self)
        self.society = Society(self)

        self.cycles: int = 0

    def setup(self) -> None:
        """
        Setup the simulation.
        1. Spawn the dooders
        2. Spawn the energy
        3. Set simulation running to true
        4. Collect initial state
        """
        self.resources.allocate_resources()
        self.society.generate_seed_population()

        self.running = True
        self.information.collect(self)
        

    def cycle(self) -> None:
        """
        Advance the simulation by one cycle.        
        """
        # place new energy
        self.resources.step()

        # advance every agent by a step
        self.time.step()

        # collect data at the end of the cycle
        self.information.collect(self)

        self.cycles += 1

    def run_simulation(self) -> None:
        """Run the simulation for a specified number of steps."""
        self.setup()

        while self.stop_conditions():
            self.cycle()

    def reset(self) -> None:
        """
        Reset the simulation object, using the current parameters.

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
        """
        Get the step results of the simulation.
        
        Returns:
            A dictionary of the results.
        """
        return self.information.get_result_dict(self)

    def generate_id(self) -> int:
        """
        Generate a new id for an object.
        
        Returns:
            A uuid4 short id.
        """
        return self.seed.uuid()

    def stop_conditions(self) -> bool:
        """
        Check if the simulation should stop.
        
        Returns:
            True if the simulation should stop, False otherwise.
        """
        result, reason = ConditionRegistry.check_conditions(self)

        if result:
            self.stop()
            self.log(1, f"Simulation stopped because of {reason}", 'Simulation')

            return False

        else:
            return True
        
    def log(self, granularity: int, message: str, scope: str) -> None:
        """ 
        Log a message to the logger.
        
        Args:
            granularity: The granularity of the message. 1 is the least granular.
            message: The message to log.
            scope: The scope of the message. Like 'Simulation' or 'Dooder'
        """
        cycle_number = self.time.time

        log_dict = {
            'scope': scope,
            'cycle_number': cycle_number,
            'granularity': granularity,
            'message': message
        }

        final_message = str(log_dict).strip('{}')
        
        self.information.log(final_message, granularity)
    
    @property
    def cycle_number(self) -> int:
        """ 
        Get the current cycle number.
        
        Returns:
            The current cycle number.
        """
        return self.cycles
