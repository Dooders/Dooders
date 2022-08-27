from typing import Dict, List

import shortuuid
from fastapi import WebSocket

from sdk.base_object import BaseObject
from sdk.parameters import ExperimentParameters
from sdk.simulation import Simulation


class Experiment:
    def __init__(self, parameters: ExperimentParameters):
        """
        Initializes an experiment.

        Args:
            parameters: Experiment parameters.
        """
        self.parameters = parameters
        self.experiment_id = shortuuid.uuid()
        self.simulation = Simulation(self.experiment_id, self.parameters)

    def setup_experiment(self) -> None:
        """ 
        Setup the experiment.    
        """
        self.simulation.setup()

    def execute_cycle(self) -> None:
        """  
        Execute a cycle. 
        """
        self.simulation.cycle()

    def get_log(self, n: int = 20):
        """ 
        Fetch the past n log entries.
        """
        with open(f"logs/log.log", "r") as f:
            lines = f.readlines()[-n:]
            for line in lines:
                if self.experiment_id in line:
                    print(line)

    def get_object(self, object_id: str) -> BaseObject:  # ! make this better
        """ 
        Fetch an object by its id.

        Args:
            object_id: The id of the object.
        """
        return self.simulation.time.get_object(object_id)

    def get_cycle_results(self) -> Dict:
        """         
        Returns:
            A dictionary of the results of the current cycle.
        """
        return self.simulation.get_results()

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
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.active_experiments: Dict[str, Experiment] = {}

    def add_experiment(self, experiment: Experiment):
        self.active_experiments[experiment.experiment_id] = experiment

    def get_experiment(self, experiment_id: str):
        return self.active_experiments[experiment_id]

    def delete_experiment(self, experiment_id: str):
        del self.active_experiments[experiment_id]

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    def cleanup(self, session_id: str):
        self.disconnect(self.active_connections[session_id])
        self.delete_experiment(session_id)
