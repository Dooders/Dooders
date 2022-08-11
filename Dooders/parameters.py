from pydantic import BaseModel

class ExperimentParameters(BaseModel):
    """
    Parameters for the simulation.
    Can be changed based on user input.

    Attributes:
        width: The width of the enviroment grid.
        height: The height of the enviroment grid.
        agents: The initial number of agents when starting the simulation.
        steps: The number of steps to run.
        verbose: Whether to print the output.
    """
    width: int = 20
    height: int = 20
    agents: int = 10
    steps: int = 100
    verbose: bool = True
    verbosity: int = 3
    initial_energy_value: int = 1
    initial_energy_count: int = 10
    

