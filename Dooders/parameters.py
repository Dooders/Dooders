from pydantic import BaseModel

class Parameters(BaseModel):
    """
    Parameters class
    """
    width: int = 20
    height: int = 20
    initial_agents: int = 10
    verbose: bool = True
    steps: int = 100
    

