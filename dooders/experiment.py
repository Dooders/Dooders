# input paramters from client
# base class for an experiment to be used in the api
# functions to start, stop, reset, etc.
from simulation import Simulation
from parameters import Parameters


class Experiment:

    def __init__(self, parameters: Parameters):
        self.parameters = parameters
        self.status = "waiting"
        self.simulation = Simulation(self.parameters)

    def start(self):
        self.status = "running"
        self.simulation.run_model()
        self.status = "finished"

    def stop(self):
        self.simulation.stop()
        self.status = "stopped"

    def reset(self):
        self.simulation.reset()
        self.status = "reset"

    @property
    def get_status(self):
        return self.status
