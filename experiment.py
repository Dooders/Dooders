from typing import List, Dict
from fastapi import WebSocket
import shortuuid

from dooders.simulation import Simulation
from dooders.parameters import ExperimentParameters


class Experiment:
    def __init__(self, parameters: ExperimentParameters):
        self.parameters = parameters
        self.verbosity = parameters.verbosity
        self.experiment_id = shortuuid.uuid()
        self.simulation = Simulation(self.experiment_id, self.parameters)


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
    

