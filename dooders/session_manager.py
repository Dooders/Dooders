from typing import Dict, List

from fastapi import WebSocket

from dooders.experiment import Experiment


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
