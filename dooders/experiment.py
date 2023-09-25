import json
import time
from typing import Callable, List, Union

from tqdm import tqdm

from dooders.sdk import strategies
from dooders.sdk.actions import *
from dooders.sdk.base.agent import Agent
from dooders.sdk.core import Assemble
from dooders.sdk.policies import *
from dooders.sdk.surfaces import *
from dooders.sdk.utils import ShortID
from dooders.sdk.utils.loggers import log_entries


class Experiment:
    """
    Class to manage the overall experiment and each simulation.

    Parameters
    ----------
    experiment_name: Union[str, None] = None
        The name of the experiment to save results. 
        If None, the experiment will not be saved.
    settings: dict = {}
        Included settings to override defaults.
    save_state: bool = False
        Whether to save experiment results.
    max_reset: int = 5
        The maximum number of times to reset the simulation.
    batch: bool = False
        Whether to run the simulation in batch mode.

    Attributes
    ----------
    seed: ShortID
        A unique identifier for the experiment.
    experiment_id: str
        The unique identifier for the experiment.
    settings: dict
        See Parameters.
    save_state: bool
        See Parameters.
    batch: bool
        See Parameters.
    max_reset: int
        See Parameters.
    gene_pool: dict
        The gene pool of the experiment. All fit Dooders will be saved after 
        each simulation
    save_folder: str
        The folder to save the experiment results in. It will be named after
        the experiment name.

    Methods
    -------
    create_simulation()
        Create a simulation.
    simulate(simulation_count: int = 1, restart: bool = False)
        Simulate a single cycle.
    batch_simulate(simulation_number: int = 100, experiment_count: int = 1, custom_logic: Callable = None, save_result: bool = False)
        Simulate n cycles.
    get_objects(object_type: str = 'Agent')
        Get all objects of a given type.
    save_object(object: Callable, filename: str)
        Save an object into a json file.
    save_logs()
        Save the logs of the experiment into a json file.
    save_passed_dooders()
        Save the internal model weights of any Dooders that made it to the end 
        of the simulation.
    save_experiment_results()
        Save the results of the experiment into a json file.

    Properties
    ----------
    logs
        Get the logs of the experiment.
    """

    experiment_results = {}

    def __init__(self,
                 experiment_name: Union[str, None] = None,
                 settings: dict = {},
                 save_state: bool = False,
                 max_reset: int = 5,
                 batch: bool = False) -> None:
        self.seed = ShortID()
        self.experiment_id = self.seed.uuid()
        self.settings = settings
        self.save_state = save_state
        self.batch = batch
        self.max_reset = max_reset
        self.gene_pool = {}
        self.save_folder = experiment_name

    def create_simulation(self) -> None:
        """
        Create a simulation.

        See the `Assemble` class for more information.

        Returns
        -------
        Simulation
            A simulation object. Through the Assembly class.
        """
        return Assemble.execute(self.settings)

    def simulate(self, simulation_count: int = 1, restart: bool = False) -> None:
        """ 
        Simulate a single cycle.

        Will restart the simulation if the simulation ends before the
        maximum number of cycles.

        Will save the state of the simulation if the save_state attribute
        is set to True.

        Parameters
        ----------
        simulation_count: int
            The number of the current simulation. Useful when running
            multiple simulations.
        """
        self.start_time = time.time()
        self.simulation = self.create_simulation()
        self.simulation.auto_restart = restart
        simulate_again = self.simulation.run_simulation(
            self.batch, simulation_count)
        if simulate_again and simulation_count < self.max_reset:
            del self.simulation
            self.simulate(simulation_count+1, restart=restart)

        elif self.save_state:
            self._save_state()

        self.end_time = time.time()

    def batch_simulate(self,
                       simulation_number: int = 100,
                       experiment_count: int = 1,
                       custom_logic: Callable = None,
                       save_result: bool = False) -> None:
        """ 
        Simulate n cycles.

        Parameters
        ----------
        simulation_number: int
            The number of simulations to run.
        experiment_count: int
            The number of the current experiment. Useful when running 
            multiple experiments.
        custom_logic: Callable
            A function to run before each simulation. 
            For any custom handling before each simulation.
        save_result: bool
            Whether to save the results of the experiment. Including logs
        """
        self.start_time = time.time()
        pbar = tqdm(
            desc=f"Experiment[{experiment_count}] Progress", total=simulation_number)
        for number in range(simulation_number):
            self.simulation = self.create_simulation()
            self.simulation.auto_restart = False

            if custom_logic:
                custom_logic(self)

            self.simulation.run_simulation(batch=True)
            self.experiment_results[number] = {}
            self.experiment_results[number]['summary'] = self.simulation.simulation_summary
            self.experiment_results[number]['state'] = self.simulation.state
            self.save_passed_dooders()
            del self.simulation
            pbar.update(1)

        pbar.close()

        if save_result:
            self.save_experiment_results()
            self.save_logs()

        self.end_time = time.time()

    def get_objects(self, object_type: str = 'Agent') -> List[Agent]:
        """ 
        Get all objects of a given type.
        Returns all objects if no type is given.

        Parameters
        ----------
        object_type: str
            The type of object to get.

        Returns
        -------
        List[Agent]
            A list of objects of the given type.
        """
        return self.simulation.environment.get_objects(object_type)

    def save_object(self, object: Callable, filename: str) -> None:
        """ 
        Save an object into a json file.

        Parameters
        ----------
        object: Callable
            The object to save.
        filename: str
            The name of the file to save the object in.
        """
        if self.save_folder is not None:
            save_path = f'experiments/{self.save_folder}/{filename}.json'

            if not os.path.exists(f'experiments/{self.save_folder}/'):
                os.makedirs(f'experiments/{self.save_folder}/')

        with open(save_path, "w") as outfile:
            json.dump(object, outfile)

    def save_logs(self) -> None:
        """ 
        Save the logs of the experiment into a json file.
        """
        self.save_object(self.logs, 'learning_log')

    def _save_state(self) -> None:
        """ 
        Save the state of the simulation into a json file.
        """
        pass

    def save_passed_dooders(self) -> None:
        """ 
        Save the internal model weights of any Dooders that 
        made it to the end of the simulation.
        """

        if self.save_folder is not None:
            setting = self.settings.get('GenePool')

            for dooder in self.get_objects('Dooder'):
                if dooder.internal_models.weights:
                    # create dooder directory if it doesn't exist
                    if setting == 'save':
                        if not os.path.exists(f"experiments/{self.save_folder}/dooders/"):
                            os.makedirs(
                                f"experiments/{self.save_folder}/dooders/")
                        dooder.internal_models.save(
                            f"experiments/{self.save_folder}/dooders/{dooder.id}")
                    elif setting == 'retain':
                        self.gene_pool[dooder.id] = dooder.internal_models.weights

    def save_experiment_results(self) -> None:
        """ 
        Save the results of the experiment into a json file.

        Parameters
        ----------
        save_folder: str
            The folder to save the results in.
        """

        self.save_object(self.experiment_results, 'experiment_results')

    @property
    def logs(self) -> dict:
        """ 
        Get the logs of the experiment.

        Returns
        -------
        dict
            The logs of the experiment.
        """
        return log_entries

    @property
    def elapsed_time(self) -> float:
        """ 
        Get the elapsed time of the experiment.

        Returns
        -------
        float
            The elapsed time of the experiment.
        """
        return self.end_time - self.start_time
