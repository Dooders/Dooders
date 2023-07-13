""" 
Simulation
----------

The simulation class is the main class of the simulation. It is responsible for
initializing the simulation, running the simulation, and displaying the results.
"""

import traceback
from datetime import datetime

from tqdm import tqdm

from dooders.sdk.base.reality import Reality
from dooders.sdk.core import Condition
from dooders.sdk.models.information import Information


class Simulation(Reality):
    """
    The simulation class is the main class of the simulation. It is responsible for
    initializing the simulation, running the simulation, and displaying the results.

    Parameters
    ----------
    settings: dict
        The settings for the simulation.
    auto_restart: bool
        Whether the simulation should restart if it fails.

    Attributes
    ----------
    running: bool
        Whether the simulation is running or not.
    cycle_number: int
        The number of cycles that have passed.

    Methods
    -------
    setup() -> None
        Setup the simulation.
    step() -> None
        Advance the simulation by one cycle.
    cycle() -> None
        Run the simulation until a condition is met.
    run_simulation() -> None
        Run the simulation until a condition is met.
    reset() -> None
        Reset the simulation.
    stop() -> None
        Stop the simulation.
    generate_id() -> str
        Generate a unique ID for the simulation.
    random_dooder() -> Dooder
        Generate a random dooder.
    stop_conditions() -> bool
        Check if the simulation should stop.
    log(granularity: int, message: str, scope: str = 'simulation') -> None
        Log a message.

    Properties
    ----------
    simulation_summary: dict
        The summary of the simulation.
    state: dict
        The state of the simulation.
    """

    def __init__(self, settings: dict, auto_restart: bool = True, batch_process: bool = True) -> None:
        super().__init__()
        self.settings = settings
        self.running = False
        self.cycle_number: int = 0
        self.auto_restart = auto_restart
        self.batch_process = batch_process
        Information._init_information(self)

    def setup(self) -> None:
        """
        Setup the simulation.
        1. Spawn the dooders
        2. Spawn the energy
        3. Set simulation running to true
        4. Collect initial state
        """
        self.resources.allocate_resources()
        self.arena.generate_seed_population()

        self.running = True

    def step(self) -> None:
        """
        Advance the simulation by one cycle.

        1. Advance every agent by a step
        2. Collect data at the end of the cycle
        3. Place new energy
        4. Collect stats
        5. Increment cycle counter   
        """
        # advance every agent by a step
        self.time.step()

        # collect data at the end of the cycle
        Information.collect(self)

        # place new energy
        self.resources.step()

        # collect stats
        self.arena.step()

        self.cycle_number += 1

    def cycle(self) -> None:
        """ 
        Advance the simulation by one cycle.
        """
        if self.stop_conditions():
            self.step()

    def run_simulation(self, batch: bool = False, simulation_count: int = 1) -> None:
        """
        Run the simulation for a specified number of steps.

        1. Setup the simulation
        2. Run the simulation until the stop conditions are met
        3. Collect the results
        """
        self.batch = batch
        max_cycles = self.settings.get('MaxCycles')

        if batch:
            disable = True
        else:
            disable = False
        pbar = tqdm(
            desc=f"Simulation[{simulation_count}] Progress", total=max_cycles, disable=disable)
        self.starting_time = datetime.now()
        try:

            while self.stop_conditions():
                self.step()
                pbar.update(1)

        except Exception as e:
            print(traceback.format_exc())
            print('Simulation failed')

        finally:
            self.ending_time = datetime.now()
            pbar.close()
            # Information.store()

        if self.cycle_number < max_cycles and self.auto_restart:
            return True

    def reset(self) -> None:
        """
        Reset the simulation object, using the current parameters.

        This is useful for resetting the simulation after a parameter change.
        """
        self.__init__(self.settings)
        Information.reset()
        self.setup()

    def stop(self) -> None:
        """
        Stop the simulation.
        """
        self.running = False

    def generate_id(self) -> int:
        """
        Generate a new id for an object.

        Returns
        -------
        int
            A new id for an object.
        """
        return self.seed.uuid()

    def random_dooder(self) -> object:
        """
        Get a random dooder from the simulation.

        Returns
        -------
        Dooder
            A random dooder from the simulation.
        """
        return self.arena.get_dooder()

    def stop_conditions(self) -> bool:
        """
        Check if the simulation should stop.

        Returns
        -------
        bool
            Whether the simulation should stop or not.
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

        Parameters
        ----------
        granularity: int
            The granularity of the message.
        message: str
            The message to log.
        scope: str
            The scope of the message.
        """
        cycle_number = self.time.time

        log_dict = {
            'Scope': scope,
            'CycleNumber': cycle_number,
            'Granularity': granularity,
            'Message': message
        }

        final_message = str(log_dict).strip('{}')

        Information.log(final_message, granularity)

    @property
    def simulation_summary(self) -> dict:
        """ 
        Get a summary of the simulation.

        Returns
        -------
        dict
            A dictionary of the summary of the simulation.
        """
        return {'SimulationID': self.simulation_id,
                'Timestamp': datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
                'CycleCount': self.cycle_number,
                'TotalEnergy': sum(Information.data['resources']['allocated_energy']),
                'ConsumedEnergy': sum(Information.data['resources']['consumed_energy']),
                'StartingDooderCount': self.settings.get('SeedCount'),
                'EndingDooderCount': len(self.arena.active_dooders),
                'ElapsedSeconds': int((self.ending_time - self.starting_time).total_seconds())
                }

    @property
    def state(self) -> dict:
        """ 
        Get the current state of the simulation.

        Returns
        -------
        dict
            The current state of the simulation.
        """
        return {
            'simulation_id': self.simulation_id,
            'running': self.running,
            'starting_time': str(self.starting_time),
            'ending_time': str(self.ending_time),
            'arena': self.arena.state,
            'environment': self.environment.state,
            'information': Information.data
        }
