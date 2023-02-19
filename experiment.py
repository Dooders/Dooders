import ast
from random import choices
from typing import Dict, List

from fastapi import WebSocket

from sdk.base.base_agent import BaseAgent
from sdk.config import ExperimentParameters
from sdk.simulation import Simulation
from sdk.utils import ShortID


class Experiment:
    """
    Class to manage the overall experiment and each simulation.

    """

    results = {}

    def __init__(self, parameters: ExperimentParameters, send_to_db=True, details=None) -> None:
        """
        Initializes an experiment.

        Args:
            parameters: Experiment parameters.

        Attributes:
            experiment_id: The id of the experiment.
            simulation: The simulation object.
            parameters: The experiment parameters.
            seed: The seed of the experiment. Used in experiment_id generation.
        """
        self.seed = ShortID()
        self.parameters = parameters
        self.experiment_id = self.seed.uuid()
        self.details = details
        self.create_simulation()

    def create_simulation(self, simulation_id: str = None) -> None:
        """
        Create a simulation.

        Args:
            simulation_id: The id of the simulation. If None, a random id will be assigned.
        """
        if simulation_id is None:
            simulation_id = self.seed.uuid()
        self.simulation = Simulation(
            simulation_id, self.experiment_id)

    def simulate(self, n: int = 1) -> None:
        """ 
        Simulate n cycles.

        Args:
            n: The number of cycles to simulate.
        """
        for i in range(n):
            simulation_id = self.seed.uuid()
            self.simulation = Simulation(
                simulation_id, self.experiment_id, self.parameters, self.send_to_db, self.details)
            self.simulation.run_simulation()
            self.results[i] = self.simulation.simulation_summary()
            # del self.simulation

    # def setup_experiment(self) -> None:
    #     """
    #     Setup the experiment.
    #     """
    #     self.simulation.setup()

    # def execute_cycle(self) -> None:
    #     """
    #     Execute a cycle.
    #     """
    #     self.simulation.cycle()

    def get_log(self) -> List[str]:
        """ 
        Fetch the log for the current experiment, append each line to logs list and return a list of dictionaries.
        """
        logs = []
        with open(f"logs/log.log", "r") as f:
            lines = f.readlines()
            for line in lines:
                if self.experiment_id in line:
                    final = line[:-2]
                    logs.append(ast.literal_eval(final))

    def print_log(self, n: int = 20) -> List[str]:
        """ 
        Print the past n log entries.
        """
        with open(f"logs/log.log", "r") as f:
            lines = f.readlines()[-n:]
            for line in lines:
                if self.experiment_id in line:
                    print(line)

    def get_object(self, object_id: str) -> BaseAgent:
        """ 
        Fetch an object by its id.

        Args:
            object_id: The id of the object. 
                Based on a random short uuid assigned to every object at its creation.

        Returns:
            The object with the given id.
        """
        return self.simulation.environment.get_object(object_id)

    def get_objects(self, object_type: str = 'BaseAgent') -> List[BaseAgent]:
        """ 
        Get all objects of a given type.
        Returns all objects if no type is given.

        Args:
            type: The type of object to get.

        Returns:
            A list of objects of the given type.
        """
        return self.simulation.environment.get_objects(object_type)

    def get_random_objects(self, object_type: str = 'BaseAgent', n: int = 1) -> List[BaseAgent]:
        """ 
        Get n random objects of a given type.
        Returns all objects if no type is given.

        Args:
            type: The type of object to get.
            n: The number of objects to get.

        Returns:
            A list of n random objects of the given type.
        """
        object_list = self.get_objects(object_type)
        k = min(len(object_list), n)
        random_objects = choices(object_list, k=k)

        return random_objects

    def get_cycle_results(self) -> Dict:
        """         
        Returns:
            A dictionary of the results of the current cycle.
        """
        return self.simulation.get_results()

    def get_dooder_history(self, object_id: str = 'Random') -> Dict:
        """
        Get the history of a dooder.
        Returns a random dooder history if no id is given.

        Args:
            object_id: The id of the dooder. If 'Random', 
                a random dooder will be selected. 

        Returns:
            A dictionary of the history of the dooder.
        """
        if object_id == 'Random':
            random_object = self.get_random_objects('Dooder')

            if random_object:
                object_id = random_object[0].id
            else:
                return 'No active Dooders'

        return self.simulation.information.get_object_history(object_id)

    def experiment_summary(self):
        """
        Returns a summary of the experiment.
        """
        return self.simulation.simulation_summary()

    @property
    def is_running(self) -> bool:
        """
        Returns:
            True if the experiment is running.
        """
        return self.simulation.running

    @property
    def cycle_number(self) -> int:
        """ 
        Returns:
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
