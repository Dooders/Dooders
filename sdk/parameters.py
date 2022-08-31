# from typing import List
# import uuid
# from pydantic import BaseModel, Field

# from sdk.base_object import BaseObject
# from sdk import Dooder, Energy, Environment, Information, Time
# from sdk.base import BaseComponent

# #! maybe make components and object their own classes?
# #! building blocks are objects and components?
# #! objects have time limits, components always persist but change.
# #! Objects and components interact with each other.


# class StopCondition(BaseModel):
#     Name: str = Field(..., description="Name of the stop condition")
#     Condition: str = Field(..., description="Condition to be met")


# class DooderParameters(BaseModel):
#     StartingEnergyCount: int = Field(..., description="Starting energy count")
#     StartingAgentCount: int = Field(..., description="Starting agent count")
#     Moore: bool = Field(...,
#                         description="Whether the dooder is a moore neighborhood")


# class EnergyConfig(BaseModel):
#     MaxLifespan: int = Field(..., description="Maximum lifespan of an energy")
#     StartingEnergyCount: int = Field(..., description="Starting energy count")

# #! should I just make this sim config class the base class for all sim?
# #! make the config be the dna, it will create the simulation based on configs and python classes


# class BaseSimulation(BaseModel):
#     MaxCycles: int = Field(..., description="Maximum number of cycles to run")
#     StopConditions: List[StopCondition] = Field(
#         ..., description="List of stop conditions")
#     CycleEnergyAdd: int = Field(..., description="Energy added per cycle")
#     Granularity: int = Field(...,
#                              description="Granularity of the information to be logged")
#     Objects: List[BaseObject] = Field(
#         ..., description="List of objects to be added to the simulation")
#     Components: List[BaseComponent] = Field(
#         ..., description="List of components to be added to the simulation")

#     def __post_init__(self):  # ! maybe this is done in simulation class
#         self.StopCriteria = [StopCondition(**x) for x in self.StopConditions]
#         # ! params will be in the object class
#         self.Objects = [x(**y)
#                         for x, y in zip(self.Objects, self.Objects.Parameters)]
#         # ! params will be in the object class
#         self.Components = [
#             x(**y) for x, y in zip(self.Components, self.Components.Parameters)]


# class InformationParameters(BaseModel):
#     Collectors = []


# class EnvironmentParameters:
#     Width: int = 10
#     Height: int = 10
#     Torus: bool = True


# class ExperimentParameters(BaseModel):
#     ExperimentID: uuid = Field(..., alias="ExperimentID")
#     SimulationParams: SimulationParameters
#     EnvironmentParams: EnvironmentParameters
#     DooderParams: DooderParameters
#     EnergyParams: EnergyParameters
#     InformationParams: InformationParameters
