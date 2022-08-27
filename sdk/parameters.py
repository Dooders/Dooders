from dataclasses import dataclass


@dataclass
class DooderParameters:
    StartingEnergyCount: int = 5
    StartingAgentCount: int = 10
    Moore: bool = True
        
@dataclass
class EnergyParameters:
    MaxLifespan: int = 10
    StartingEnergyCount: int = 10
        
@dataclass
class SimulationParameters:
    MaxCycles: int = 100
    StopCriteria = []
    CycleEnergyAdd: int = 10
    Granularity: int = 2
    
@dataclass
class InformationParameters:
    Collectors = []
    
@dataclass
class EnvironmentParameters:
    Width: int = 10
    Height: int = 10
    Torus: bool = True
        

ExperimentParameters = {
    'Simulation': SimulationParameters,
    'Environment': EnvironmentParameters,
    'Dooder': DooderParameters,
    'Energy': EnergyParameters,
    'Information': EnvironmentParameters,
}
    