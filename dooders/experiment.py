import ast
import json
import shutil
from random import choices
from typing import Dict, List

from fastapi import WebSocket

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

    Methods
    -------
    create_simulation()
        Create a simulation.
    simulate()
        Simulate a single cycle.
    batch_simulate(n: int = 1)
        Simulate n cycles.  
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

    def __init__(self, settings: dict = {}, save_state: bool = False) -> None:
        self.seed = ShortID()
        self.experiment_id = self.seed.uuid()
        self.settings = settings
        self.save_state = save_state

    def create_simulation(self) -> None:
        """
        Create a simulation.

        Returns
        -------
        Simulation
            A simulation object. Through the Assembly class.
        """
        return Assemble.execute(self.settings)

    def simulate(self) -> None:
        """ 
        Simulate a single cycle.
        """
        self.simulation = self.create_simulation()
        self.simulation.run_simulation()
        if self.save_state:
            self._save_state()

    def _save_state(self) -> None:
        """ 
        Save the state of the simulation into a json file.
        """
        with open("recent/state.json", "w") as f:
            json.dump(self.simulation.state, f)

    def batch_simulate(self, n: int = 1) -> None:
        """ 
        Simulate n cycles.

        Parameters
        ----------
        n: int
            The number of simulations to run.
        """
        for i in range(n):
            self.simulation = self.create_simulation(self.settings)
            self.simulation.run_simulation()
            self.results[i] = self.simulation.simulation_summary()
            del self.simulation

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
