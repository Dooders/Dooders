from random import choices
from typing import Dict, List

from fastapi import WebSocket

from sdk.base_object import BaseObject
from sdk.config import ExperimentParameters
from sdk.simulation import Simulation
from sdk.util import ShortUUID


class Experiment:
    def __init__(self, parameters: ExperimentParameters):
        """
        Initializes an experiment.

        Args:
            parameters: Experiment parameters.
        """
        self.seed = ShortUUID()
        self.parameters = parameters
        self.experiment_id = self.seed.uuid()
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
            object_id: The id of the object. Based on a random short uuid assigned to every object at its creation.
        """
        return self.simulation.environment.get_object(object_id)
    
    def get_objects(self, object_type: str ='BaseObject') -> List[BaseObject]:
        """ 
        Get all objects of a given type.

        Args:
            type: The type of object to get.
        """
        return self.simulation.environment.get_objects(object_type)
    
    
    def get_random_objects(self, object_type: str ='BaseObject', n: int = 1) -> List[BaseObject]:
        """ 
        Get n random objects of a given type.

        Args:
            type: The type of object to get.
            n: The number of objects to get.
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
        
        Args:
            object_id: The id of the dooder. If 'Random', a random dooder will be selected. 
        
        Returns:
            A dictionary of the history of the dooder.
        """
        if object_id == 'Random':
            random_object = self.get_random_objects('Dooder')
            
            if random_object:
                object_id = random_object[0].unique_id
            else:
                return 'No active Dooders'
            
        return self.simulation.information.get_object_history(object_id)

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
