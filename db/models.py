from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Text, String


Base = declarative_base()

    
class SimulationSummary(Base):
    
    __tablename__ = "SimulationSummary"
    
    ExperimentID = Column(String(255), primary_key=True)
    CycleCount = Column(Integer, nullable=False)
    TotalEnergy = Column(Integer, nullable=False)
    DissipatedEnergy = Column(Integer, nullable=False)
    ConsumedEnergy = Column(Integer, nullable=False)
    StartingDooderCount = Column(Integer, nullable=False)
    EndingDooderCount = Column(Integer, nullable=False)
    
    def __init__(self, 
                 ExperimentID, 
                 CycleCount, 
                 TotalEnergy, 
                 DissipatedEnergy, 
                 ConsumedEnergy, 
                 StartingDooderCount, 
                 EndingDooderCount):
        
        self.ExperimentID = ExperimentID
        self.CycleCount = CycleCount
        self.TotalEnergy = TotalEnergy
        self.DissipatedEnergy = DissipatedEnergy
        self.ConsumedEnergy = ConsumedEnergy
        self.StartingDooderCount = StartingDooderCount
        self.EndingDooderCount = EndingDooderCount


class CycleResults(Base):
    
    __tablename__ = "CycleResults"
    
    ExperimentID = Column(String(255), primary_key=True)
    CycleNumber = Column(Integer, nullable=False)
    DooderCount = Column(Integer, nullable=False)
    EnergyCount = Column(Integer, nullable=False)
    TotalDooderEnergySupply = Column(Integer, nullable=False)
    AverageEnergyAge = Column(Integer, nullable=False)

    
    def __init__(self, 
                 ExperimentID, 
                 CycleNumber, 
                 DooderCount, 
                 EnergyCount, 
                 TotalDooderEnergySupply, 
                 AverageEnergyAge):
        
        self.ExperimentID = ExperimentID
        self.CycleNumber = CycleNumber
        self.DooderCount = DooderCount
        self.EnergyCount = EnergyCount
        self.TotalDooderEnergySupply = TotalDooderEnergySupply
        self.AverageEnergyAge = AverageEnergyAge