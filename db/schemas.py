from pydantic import BaseModel


class SimulationTables(BaseModel):
    SimulationSummary: SimulationSummary
    CycleResults: CycleResults

class SimulationSummary(BaseModel):
    ExperimentID: str
    CycleCount: int
    TotalEnergy: int
    DissipatedEnergy: int
    ConsumedEnergy: int
    StartingDooderCount: int
    EndingDooderCount: int
    
    
class CycleResults(BaseModel):
    ExperimentID: str
    CycleNumber: int
    DooderCount: int
    EnergyCount: int
    TotalDooderEnergySupply: int
    AverageEnergyAge: float
