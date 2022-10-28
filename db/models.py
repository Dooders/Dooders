from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import DateTime, Integer, String, Text


class RecordTypes:
    CycleResults = CycleResults
    SimulationSummary = SimulationSummary
    SimulationLogs = SimulationLogs
    DooderResults = DooderResults


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


class DooderResults(Base):

    __tablename__ = "DooderResults"

    # ExperimentID = Column(String(255), primary_key=True)
    UniqueID = Column(String(255), primary_key=True)
    CycleNumber = Column(Integer, nullable=False)
    Position = Column(String(255), nullable=False)
    EnergySupply = Column(Integer, nullable=False)
    Direction = Column(String(255), nullable=False)
    Age = Column(Integer, nullable=False)

    def __init__(self,
                 ExperimentID,
                 UniqueID,
                 CycleNumber,
                 Position,
                 EnergySupply,
                 Direction,
                 Age):

        # self.ExperimentID = ExperimentID
        self.UniqueID = UniqueID
        self.CycleNumber = CycleNumber
        self.Position = Position
        self.EnergySupply = EnergySupply
        self.Direction = Direction
        self.Age = Age


class SimulationLogs(Base):

    __tablename__ = "SimulationLogs"

    ExperimentID = Column(String(255), primary_key=True)
    Scope = Column(String(255), nullable=False)
    ID = Column(String(255), nullable=False)
    CycleNumber = Column(Integer, nullable=False)
    Granularity = Column(String(255), nullable=False)
    Message = Column(Text, nullable=False)
    Timestamp = Column(DateTime, nullable=False)

    def __init__(self,
                 ExperimentID,
                 Scope,
                 ID,
                 CycleNumber,
                 Granularity,
                 Message,
                 Timestamp):

        self.ExperimentID = ExperimentID
        self.Scope = Scope
        self.ID = ID
        self.CycleNumber = CycleNumber
        self.Granularity = Granularity
        self.Message = Message
        self.Timestamp = Timestamp
