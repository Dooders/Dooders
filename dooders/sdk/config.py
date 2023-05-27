from dataclasses import dataclass
from typing import Callable, Dict, List

import yaml
from pydantic import BaseModel, Field


class BaseCollector(BaseModel):
    """ Base class for all collectors """
    name: str = Field(..., description="Name of the collector")
    function: Callable = Field(..., description="Function to be called")
    component: str = Field(..., description="Component type to collect")
    
# with open("sdk/config.yml", "r") as f:
#       default_config = yaml.load(f, Loader=yaml.FullLoader)



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
    Reproduction: str = Field("AverageWeights", description="Reproduction policy")
    
    
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
    

@dataclass
class ValueGenerator:
    distribution_type: str
    min_value: int
    max_value: int
    
class Config:
    """ 
    Class to hold the settings for the simulation
    
    Attributes
    ----------
    settings : dict
        Dictionary of settings
        
    Methods
    -------
    update(new_settings: dict) -> None
        Update the settings with new settings
    get(setting_name: str) -> object
        Get a setting from the settings
    """
    def __init__(self) -> None:
        self.settings: dict = {
            'MaxCycles': 100,
            'SeedCount': 1,
            'EnergyPerCycle': ValueGenerator('uniform', 5, 10),
            'MaxTotalEnergy': 10,
            'GridHeight': 5,
            'GridWidth': 5,
            'EnergyLifespan': ValueGenerator('uniform', 2, 5),
        }

    def update(self, new_settings: dict) -> None:
        """ 
        Update the settings with new settings
        
        Parameters
        ----------
        new_settings : dict
            New settings to update the current settings with
        """
        for key, value in new_settings.items():
            if key in self.settings:
                self.settings[key] = value
            else:
                raise KeyError(f"{key} does not exist in the settings")

    def get(self, setting_name: str) -> object:
        """ 
        Get a setting from the settings
        
        Parameters
        ----------
        setting_name : str
            Name of the setting to get
        """
        try:
            return self.settings[setting_name]
        except KeyError:
            raise KeyError(f"{setting_name} does not exist in the settings")

