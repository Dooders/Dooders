import yaml
from typing import Callable, List

from pydantic import BaseModel, Field

#! Need better config, and a way to change settings on the fly
#! will also need a settings view on the front-end


class BaseCollector(BaseModel):
    """ Base class for all collectors """
    name: str = Field(..., description="Name of the collector")
    function: Callable = Field(..., description="Function to be called")
    component: str = Field(..., description="Component type to collect")
    
with open("sdk/config.yml", "r") as f:
      default_config = yaml.load(f, Loader=yaml.FullLoader)



#### Parameters #####
class DooderParameters(BaseModel):
    """ Parameters for Dooder object """
    StartingEnergySupply: int = Field(5, description="Starting energy count")
    StartingAgentCount: int = Field(10, description="Starting agent count")
    Moore: bool = Field(True, description="If the dooder is a moore neighborhood")

class EnergyParameters(BaseModel):
    """ Parameters for Energy object """
    # Random value between Min and Max lifecycle
    MaxEnergyLife: int = Field(10, description="Maximum lifespan of an energy")
    MinEnergyLife: int = Field(2, description="Minimum lifespan of an energy")
    StartingEnergyCount: int = Field(10, description="Starting energy count")

class SimulationParameters(BaseModel):
    """ Parameters for the Simulation """
    MaxCycles: int = Field(100, description="Maximum number of cycles to run")
    # StopConditions: List[StopCondition] = Field(None, description="List of stop conditions")
    EnergyPerCycle: int = Field(10, description="Energy added per cycle")

class InformationParameters(BaseModel):
    """ Parameters for the Information component """
    Collectors: List[str] = []
    Granularity: int = Field(2, description="Granularity of the log")

class EnvironmentParameters(BaseModel):
    """ Parameters for the Environment component """
    Width: int = Field(10, description="Width of the environment")
    Height: int = Field(10, description="Height of the environment")
    Torus: bool = Field(True, description="Whether the environment is torus")


class PolicyParameters(BaseModel):
    Movement: str = Field("RuleBased", description="Move policy")
    
    
    
    
class ExperimentParameters(BaseModel):
    """ Parameters for the Experiment """
    Simulation = SimulationParameters()
    Environment = EnvironmentParameters()
    Dooder = DooderParameters()
    Energy = EnergyParameters()
    Information = InformationParameters()
    Policies = PolicyParameters()
    
    def get(self, key: str) -> object:
        """ 
        Get a parameter from the experiment parameters
        
        Args:
            key (str): Key to get from the parameters
        
        Returns:
            object: Value of the key
        """
        return self.__dict__[key]
