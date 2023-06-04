from typing import List

from pydantic import BaseModel


class SummaryTableSchema(BaseModel):
    SimulationID: str
    Timestamp: str
    CycleCount: int
    TotalEnergy: int
    ConsumedEnergy: int
    StartingDooderCount: int
    EndingDooderCount: int
    ElapsedSeconds: int
    StartingTime: str
    EndingTime: int
        
class ArenaTableSchema(BaseModel):
    DooderID: str
    Number: int
    Hunger: int
    Age: int
    Generation: int
    Birth: int
    Death: int
    ReproductionCount: int
    MoveCount: int
    EnergyConsumed: int
    Tag: str

class GeneEmbeddingTableSchema(BaseModel):
    DooderID: str
    CycleNumber: int
    X: float
    Y: float
    Z: float
        
class InferenceRecordTableSchema(BaseModel):
    DooderID: str
    CycleNumber: int
    Action: str
    Perception: List[str]
    Decision: str
    Reality: List[str]
    InferredGoal: str
    Accurate: bool