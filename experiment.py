from typing import Dict, List

import shortuuid
from fastapi import WebSocket

from sdk.dooder import Dooder
from sdk.environment.energy import Energy
from sdk.parameters import ExperimentParameters
from sdk.simulation import Simulation


class Experiment:
    def __init__(self, parameters: ExperimentParameters):
        self.parameters = parameters
        self.experiment_id = shortuuid.uuid()
        self.simulation = Simulation(self.experiment_id, self.parameters)

    def get_log(self, n: int = 20):
        with open(f"logs/log.log", "r") as f:
            lines = f.readlines()[-n:]
            for line in lines:
                if self.experiment_id in line:
                    print(line)

    def get_dooder(self, dooder_id: int):
        dooder = [object for object in self.simulation.time._objects if isinstance(
            object, Dooder) and object.unique_id == dooder_id]
        return dooder[0].__dict__ if dooder else 'Not Found'

    def get_energy(self, energy_id: int):
        energy = [object for object in self.simulation.time._objects if isinstance(
            object, Energy) and object.unique_id == energy_id]
        return energy[0].__dict__ if energy else 'Not Found'

    def get_object(self, object_id: str):  # ! make this better
        return self.simulation.time.get_object(object_id)
    
    def get_results(self):
        return self.simulation.information.cycle_results()


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
