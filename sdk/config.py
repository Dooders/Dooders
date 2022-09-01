import json
from typing import Callable, List
from pydantic import BaseModel, Field


class BaseCollector(BaseModel):
    name: str = Field(..., description="Name of the collector")
    function: Callable = Field(..., description="Function to be called")
    component: str = Field(..., description="Component type to collect")
    
    
with open("sdk/config.json", "r") as f:
     default_config = json.load(f)


    
##### Stop Conditions ##### 
#! need to write tests for these
class StopCondition(BaseModel):
    Name: str = Field(..., description="Name of the stop condition")
    Condition: str = Field(..., description="Condition to be met")
    
def check_max_cycle(simulation):
    if simulation.cycle >= simulation.params.Simulation.MaxCycles:
        return True
    
def check_simulation_running(simulation):
    if not simulation.running:
        return True
    
def check_dooder_count(simulation):
    if simulation.environment.get_objects("Dooder").count() == 0:
        return True
    
class MaxCyclesCheck:
    Name = "Stop on Max Cycles"
    Condition = check_max_cycle
    
class StopRunningCheck:
    Name = "Stop on Max Cycles"
    Condition = check_simulation_running
    
class StopDooderZeroCheck:
    Name = "Stop on zero Dooder objects"
    Condition = check_dooder_count



#### Parameters #####

class DooderParameters(BaseModel):
    StartingEnergySupply: int = Field(5, description="Starting energy count")
    StartingAgentCount: int = Field(10, description="Starting agent count")
    Moore: bool = Field(True, description="If the dooder is a moore neighborhood")


class EnergyParameters(BaseModel):
    # Random value between Min and Max lifecycle
    MaxLifespan: int = Field(10, description="Maximum lifespan of an energy")
    MinLifeSpan: int = Field(2, description="Minimum lifespan of an energy")
    StartingEnergyCount: int = Field(10, description="Starting energy count")


class SimulationParameters(BaseModel):
    MaxCycles: int = Field(100, description="Maximum number of cycles to run")
    StopConditions: List[StopCondition] = Field(None, description="List of stop conditions")
    CycleEnergyAdd: int = Field(10, description="Energy added per cycle")
    Granularity: int = Field(2, description="Granularity of the log")


class InformationParameters(BaseModel):
    Collectors: List[str] = []


class EnvironmentParameters(BaseModel):
    Width: int = Field(10, description="Width of the environment")
    Height: int = Field(10, description="Height of the environment")
    Torus: bool = Field(True, description="Whether the environment is torus")


class ExperimentParameters(BaseModel):
    Simulation = SimulationParameters()
    Environment = EnvironmentParameters()
    Dooder = DooderParameters()
    Energy = EnergyParameters()
    Information = InformationParameters()
    
    def get(self, key: str) -> object:
        return self.__dict__[key]
