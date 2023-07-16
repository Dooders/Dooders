import ast
import json
import shutil
from random import choices
from typing import Callable, Dict, List

from fastapi import WebSocket
from tqdm import tqdm

from dooders.sdk import strategies
from dooders.sdk.actions import *
from dooders.sdk.base.agent import Agent
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
    experiment_id: str
        The id of the experiment.
    seed: ShortID
        A `ShortID` object to generate random ids.
    settings: dict
        The settings of the experiment.
    save_state: bool
        Whether to save the state of the simulation.
    batch: bool
        Whether to run the simulation in batch mode.
    max_reset: int
        The maximum number of times to reset the simulation.
    simulation: Simulation
        The simulation object.

    Methods
    -------
    create_simulation()
        Create a simulation.
    simulate()
        Simulate a single cycle.
    batch_simulate(n: int = 1)
        Simulate n cycles.  
    cleanup()
        Remove all contents of the 'recent' directory.
    save_experiment_results(save_folder: str = 'recent/')
        Save the results of the experiment into a json file.
    get_log()
        Fetch the log for the current experiment, append each line to logs list and return a list of dictionaries.
    print_log(n: int = 20)
        Print the past n log entries.
    get_object(object_id: str)
        Fetch an object by its id.
    get_objects(object_type: str = 'Agent')
        Fetch all objects of a given type.   
    """

    results = {}

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

        Returns
        -------
        Simulation
            A simulation object. Through the Assembly class.
        """
        return Assemble.execute(self.settings)

    def simulate(self, simulation_count: int = 1) -> None:
        """ 
        Simulate a single cycle.
        """
        self.simulation = self.create_simulation()
        restart = self.simulation.run_simulation(self.batch, simulation_count)
        if restart and simulation_count < self.max_reset:
            self.cleanup()
            del self.simulation
            self.simulate(simulation_count+1)

        elif self.save_state:
            self._save_state()

    def cleanup(self) -> None:
        """ 
        Remove all contents of the 'recent' directory
        """

        folder = 'recent/dooders/'  # replace with your folder path

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

    def batch_simulate(self,
                       n: int = 100,
                       experiment_count: int = 1,
                       save_folder: str = 'recent/',
                       custom_logic: Callable = None) -> None:
        """ 
        Simulate n cycles.

        Parameters
        ----------
        n: int
            The number of simulations to run.
        save_folder: str
            The folder to save the results in.
        custom_logic: Callable
            A function to run before each simulation. 
            For any custom handling before each simulation.
        """

        pbar = tqdm(desc=f"Experiment[{experiment_count}] Progress", total=n)
        for i in range(n):
            self.simulation = self.create_simulation()
            self.simulation.auto_restart = False

            if custom_logic:
                custom_logic(self)

            self.simulation.run_simulation(batch=True)
            self.results[i] = {}
            self.results[i]['summary'] = self.simulation.simulation_summary
            self.results[i]['state'] = self.simulation.state
            self.save_passed_dooders(save_folder)
            del self.simulation
            pbar.update(1)

        pbar.close()
        self.save_experiment_results(save_folder)

    def save_passed_dooders(self, save_folder: str) -> None:
        """ 
        Save the internal model weights of any Dooders that 
        made it to the end of the simulation.
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
            json.dump(self.results, outfile)

    def get_log(self) -> List[str]:
        """ 
        Fetch the log for the current experiment, append each 
        line to logs list and return a list of dictionaries.

        Returns
        -------
        List[str]
            A list of dictionaries containing the log entries.
        """
        logs = []
        with open(f"logs/log.json", "r") as f:
            lines = f.readlines()
            for line in lines:
                logs.append(ast.literal_eval(line))

    def print_log(self, n: int = 20) -> List[str]:
        """ 
        Print the past n log entries.

        Parameters
        ----------
        n: int
            The number of log entries to print.

        Returns
        -------
        List[str]
            A list of dictionaries containing the log entries.
        """
        with open(f"logs/log.log", "r") as f:
            lines = f.readlines()[-n:]
            for line in lines:
                if self.experiment_id in line:
                    print(line)

    def get_object(self, object_id: str) -> Agent:
        """ 
        Fetch an object by its id.

        Parameters
        ----------
        object_id: str
            The id of the object.

        Returns
        -------
        Agent
            The object with the given id.
        """
        return self.simulation.environment.get_object(object_id)

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

    def get_random_objects(self,
                           object_type: str = 'Agent',
                           n: int = 1) -> List[Agent]:
        """ 
        Get n random objects of a given type.
        Returns all objects if no type is given.

        Parameters
        ----------
        object_type: str
            The type of object to get.
        n: int
            The number of objects to get.

        Returns
        -------
        List[Agent]
            A list of n random objects of the given type.
        """
        object_list = self.get_objects(object_type)
        k = min(len(object_list), n)
        random_objects = choices(object_list, k=k)

        return random_objects

    def get_cycle_results(self) -> Dict:
        """         
        Get the results of the current cycle.

        Returns
        -------
        Dict
            A dictionary of the results of the current cycle.
        """
        return self.simulation.get_results()

    def get_dooder_history(self, object_id: str = 'Random') -> Dict:
        """
        Get the history of a dooder.
        Returns a random dooder history if no id is given.

        Parameters
        ----------
        object_id: str
            The id of the dooder.

        Returns
        -------
        Dict
            A dictionary of the history of the dooder.
        """
        if object_id == 'Random':
            random_object = self.get_random_objects('Dooder')

            if random_object:
                object_id = random_object[0].id
            else:
                return 'No active Dooders'

        return self.simulation.information.get_object_history(object_id)

    def experiment_summary(self) -> Dict:
        """
        Returns a summary of the experiment.

        Returns
        -------
        Dict
            A dictionary of the experiment summary.
        """
        return self.simulation.simulation_summary

    def save(self, experiment_name):
        folder_path = f"experiments/{experiment_name}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(f"{folder_path}/state.json", "w") as f:
            json.dump(self.simulation.state, f)

        shutil.copyfile("logs/log.json", f"{folder_path}/log.json")

        with open(f"{folder_path}/summary.json", "w") as f:
            json.dump(self.experiment_summary(), f)

    @property
    def is_running(self) -> bool:
        """
        Returns
        -------
        bool
            True if the simulation is running, False otherwise.
        """
        return self.simulation.running

    @property
    def cycle_number(self) -> int:
        """ 
        Returns
        -------
        int:
            The current cycle number. 
        """
        return self.simulation.time.time


class SessionManager:
    """ 
    Class to manage distinct sessions and interact with the experiments.
    """

    def __init__(self):
        """ 
        Initializes the session manager.

        Attributes:
            active_experiments: A dictionary of active experiments.
            active_connections: A list of active websocket objects.
        """
        self.active_connections: List[WebSocket] = []
        self.active_experiments: Dict[str, Experiment] = {}

    def add_experiment(self, experiment: Experiment) -> None:
        """ 
        Add an experiment to the active experiments.
        """
        self.active_experiments[experiment.experiment_id] = experiment

    def get_experiment(self, experiment_id: str) -> Experiment:
        """ 
        Get an experiment by its id.

        Args:
            experiment_id: The id of the experiment.

        Returns:
            The experiment with the given id.
        """
        return self.active_experiments[experiment_id]

    def delete_experiment(self, experiment_id: str) -> None:
        """
        Delete an experiment from the active experiments.

        Args:
            experiment_id: The id of the experiment.
        """
        del self.active_experiments[experiment_id]

    async def connect(self, websocket: WebSocket) -> None:
        """ 
        Connect a websocket to the session manager.

        Args:
            websocket: The websocket to connect.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """ 
        Disconnect a websocket from the session manager.

        Args:
            websocket: The websocket to disconnect.
        """
        self.active_connections.remove(websocket)

    def cleanup(self, session_id: str) -> None:
        """  
        Cleanup the session manager.

        Args:
            session_id: The id of the session to cleanup.
        """
        self.disconnect(self.active_connections[session_id])
        self.delete_experiment(session_id)
