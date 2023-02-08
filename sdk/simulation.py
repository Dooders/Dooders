""" 
Simulation
----------

The simulation class is the main class of the simulation. It is responsible for
initializing the simulation, running the simulation, and displaying the results.
"""

import traceback
from datetime import datetime
from statistics import mean

import pandas as pd

from db.main import DB
from sdk.base.reality import Reality
from sdk.config import ExperimentParameters
from sdk.core import Condition, Policy, Step, Strategy
from sdk.core.action import Action
from sdk.models.resources import Resources
from sdk.models.society import Society


class Simulation(Reality):
    """

    """

    def __init__(
            self,
            simulation_id: str,
            experiment_id: str,
            params: ExperimentParameters,
            send_to_db=False) -> None:
        """
        Primary class to handle the simulation. A simulation will have access to 
        many different models

        Args:
            experiment_id: The id of the experiment this simulation is a part of.
            params: Experiment parameters.

        Attributes:
            cycles: The number of cycles that have passed.
        """
        super().__init__(simulation_id, experiment_id, params)

        self.strategy = Strategy()
        self.resources = Resources(self)
        self.society = Society(self)
        self.policies = Policy()
        self.actions = Action()
        self.steps = Step()
        self.running = False
        self.send_to_db = send_to_db
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

    def step(self) -> None:
        """
        Advance the simulation by one cycle.        
        """
        # advance every agent by a step
        self.time.step()

        # collect data at the end of the cycle
        self.information.collect(self)
        
        # place new energy
        self.resources.step()

        # collect stats
        self.society.step()

        self.cycles += 1

    def cycle(self) -> None:
        if self.stop_conditions():
            self.step()

    def run_simulation(self) -> None:
        """Run the simulation for a specified number of steps."""
        try:
            self.setup()

            while self.stop_conditions():
                self.step()
        except Exception as e:
            print(traceback.format_exc())
            print('Simulation failed')

        finally:
            if self.send_to_db:
                self.post_simulation()

    def post_simulation(self) -> None:
        """
        Post cycle processes. Like sending data to a postgres db

        #! better way to send data to db
        """
        df = self.information.get_dataframe('dooder')
        df['SimulationID'] = self.simulation_id
        DB.df_to_db(df, 'DooderResults')
        # df = self.information.get_dataframe('simulation')
        # Postgres.df_to_db(df, 'SimulationResults')
        logs = self.information.get_log()
        df = pd.DataFrame(logs)
        DB.df_to_db(df, 'SimulationLogs')
        summary = self.simulation_summary()
        summary['Details'] = self.details
        summary['ExperimentID'] = self.experiment_id
        DB.add_record(summary, 'SimulationSummary')

    def reset(self) -> None:
        """
        Reset the simulation object, using the current parameters.

        This is useful for resetting the simulation after a parameter change.
        """
        self.__init__(self.simulation_id, self.params)

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

    def random_dooder(self):
        """
        Get a random dooder from the simulation.

        Returns:
            A random dooder.
        """
        return self.society.get_dooder()

    def stop_conditions(self) -> bool:
        #! maybe make a decorator to implement this nicely
        """
        Check if the simulation should stop.

        Returns:
            True if the simulation should stop, False otherwise.
        """
        result, reason = Condition.check('stop', self)

        if result:
            self.stop()
            self.log(
                1, f"Simulation stopped because of {reason}", 'Simulation')

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
            'Scope': scope,
            'CycleNumber': cycle_number,
            'Granularity': granularity,
            'Message': message
        }

        final_message = str(log_dict).strip('{}')

        self.information.log(final_message, granularity)

    def simulation_summary(self):
        return {'SimulationID': self.simulation_id,
                'Timestamp': datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
                'CycleCount': self.cycles,
                'TotalEnergy': sum(self.information.data['resources']['allocated_energy']),
                'ConsumedEnergy': sum(self.information.data['resources']['consumed_energy']),
                'StartingDooderCount': self.information.data['society']['created_dooder_count'][0],
                'EndingDooderCount': len(self.society.active_dooders),
                # 'AverageAge': int(mean([d.age for d in self.society.graveyard.values()])),
                }

    @property
    def cycle_number(self) -> int:
        """ 
        Get the current cycle number.

        Returns:
            The current cycle number.
        """
        return self.cycles
