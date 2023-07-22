import json
import shutil
from typing import Callable

from tqdm import tqdm

from dooders.sdk import strategies
from dooders.sdk.actions import *
from dooders.sdk.core import Assemble
from dooders.sdk.policies import *
from dooders.sdk.surfaces import *
from dooders.sdk.utils import ShortID


class Experiment:
    """
    Class to manage the overall experiment and each simulation.

    Parameters
    ----------
    settings: dict
        The settings of the experiment.

    Attributes
    ----------
    seed: ShortID
        A unique identifier for the experiment.
    experiment_id: str
        The unique identifier for the experiment.
    settings: dict
        The settings of the experiment.
    save_state: bool
        Whether to save the state of the simulation.
    batch: bool
        Whether to run the simulation in batch mode.
    max_reset: int
        The maximum number of times to reset the simulation.
    gene_pool: dict
        The gene pool of the experiment.
    experiment_results: dict
        The results of the experiment.

    Methods
    -------
    create_simulation()
        Create a simulation.
    simulate(simulation_count: int = 1)
        Simulate a single cycle.
    batch_simulate(simulation_number: int = 100,
                     experiment_count: int = 1,
                        save_folder: str = 'recent/',
                        custom_logic: Callable = None)
        Simulate n cycles.
    cleanup()
        Remove all contents of the 'recent' directory.
    _save_state()
        Save the state of the simulation into a json file.
    save_passed_dooders(save_folder: str)
        Save the internal model weights of any Dooders that
        made it to the end of the simulation.
    save_experiment_results(save_folder: str)
        Save the results of the experiment into a json file.
    """

    experiment_results = {}

    def __init__(self,
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

    def simulate(self, simulation_count: int = 1) -> None:
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
        self.simulation = self.create_simulation()
        restart = self.simulation.run_simulation(self.batch, simulation_count)
        if restart and simulation_count < self.max_reset:
            self.cleanup()
            del self.simulation
            self.simulate(simulation_count+1)

        elif self.save_state:
            self._save_state()

    def batch_simulate(self,
                       simulation_number: int = 100,
                       experiment_count: int = 1,
                       save_folder: str = 'recent/',
                       custom_logic: Callable = None) -> None:
        """ 
        Simulate n cycles.

        Parameters
        ----------
        simulation_number: int
            The number of simulations to run.
        experiment_count: int
            The number of the current experiment. Useful when running 
            multiple experiments.
        save_folder: str
            The folder to save the results in.
        custom_logic: Callable
            A function to run before each simulation. 
            For any custom handling before each simulation.
        """

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
            self.save_passed_dooders(save_folder)
            del self.simulation
            pbar.update(1)

        pbar.close()
        self.save_experiment_results(save_folder)

    def cleanup(self) -> None:
        """ 
        Remove all contents of the 'recent' directory
        """

        folder = 'recent/dooders/'

        # iterate over all files in the folder
        for filename in os.listdir(folder):
            # construct full file path
            file_path = os.path.join(folder, filename)
            # remove the file
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                pass

    def _save_state(self) -> None:
        """ 
        Save the state of the simulation into a json file.
        """
        with open("recent/state.json", "w") as f:
            json.dump(self.simulation.state, f)

    def save_passed_dooders(self, save_folder: str) -> None:
        """ 
        Save the internal model weights of any Dooders that 
        made it to the end of the simulation.

        Parameters
        ----------
        save_folder: str
            The folder to save the results in.
        """
        setting = self.settings.get('GenePool')

        for dooder in self.get_objects('Dooder'):
            if dooder.internal_models.weights:
                # create dooder directory if it doesn't exist
                if setting == 'save':
                    if not os.path.exists(f"experiments/{save_folder}/dooders/"):
                        os.makedirs(f"experiments/{save_folder}/dooders/")
                    dooder.internal_models.save(
                        f"experiments/{save_folder}/dooders/{dooder.id}")
                elif setting == 'retain':
                    self.gene_pool[dooder.id] = dooder.internal_models.weights

    def save_experiment_results(self, save_folder: str) -> None:
        """ 
        Save the results of the experiment into a json file.

        Parameters
        ----------
        save_folder: str
            The folder to save the results in.
        """
        if save_folder == 'recent/':
            save_path = 'recent/experiment_results.json'

        else:
            save_path = f'experiments/{save_folder}/experiment_results.json'

            if not os.path.exists(f'experiments/{save_folder}/'):
                os.makedirs(f'experiments/{save_folder}/')

        with open(save_path, "w") as outfile:
            json.dump(self.experiment_results, outfile)
