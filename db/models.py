from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import DateTime, Integer, String, Text

Base = declarative_base()


class SimulationSummary(Base):

    __tablename__ = "SimulationSummary"

    ExperimentID = Column(String(255), nullable=False)
    SimulationID = Column(String(255), primary_key=True)
    Timestamp = Column(DateTime)
    CycleCount = Column(Integer, nullable=False)
    TotalEnergy = Column(Integer, nullable=False)
    DissipatedEnergy = Column(Integer, nullable=False)
    ConsumedEnergy = Column(Integer, nullable=False)
    StartingDooderCount = Column(Integer, nullable=False)
    EndingDooderCount = Column(Integer, nullable=False)
    AverageAge = Column(Integer, nullable=False)
    Details = Column(postgresql.JSONB, nullable=False)

    def __init__(self,
                 ExperimentID,
                 SimulationID,
                 Timestamp,
                 CycleCount,
                 TotalEnergy,
                 DissipatedEnergy,
                 ConsumedEnergy,
                 StartingDooderCount,
                 EndingDooderCount,
                 AverageAge,
                 Details):

        self.ExperimentID = ExperimentID
        self.SimulationID = SimulationID
        self.CycleCount = CycleCount
        self.Timestamp = Timestamp
        self.TotalEnergy = TotalEnergy
        self.DissipatedEnergy = DissipatedEnergy
        self.ConsumedEnergy = ConsumedEnergy
        self.StartingDooderCount = StartingDooderCount
        self.EndingDooderCount = EndingDooderCount
        self.AverageAge = AverageAge
        self.Details = Details


class CycleResults(Base):

    __tablename__ = "CycleResults"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    SimulationID = Column(String(255), nullable=False)
    CycleNumber = Column(Integer, nullable=False)
    DooderCount = Column(Integer, nullable=False)
    EnergyCount = Column(Integer, nullable=False)
    TotalDooderEnergySupply = Column(Integer, nullable=False)
    AverageEnergyAge = Column(Integer, nullable=False)

    def __init__(self,
                 ID,
                 SimulationID,
                 CycleNumber,
                 DooderCount,
                 EnergyCount,
                 TotalDooderEnergySupply,
                 AverageEnergyAge):

        self.SimulationID = SimulationID
        self.CycleNumber = CycleNumber
        self.DooderCount = DooderCount
        self.EnergyCount = EnergyCount
        self.TotalDooderEnergySupply = TotalDooderEnergySupply
        self.AverageEnergyAge = AverageEnergyAge


class DooderResults(Base):

    __tablename__ = "DooderResults"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    SimulationID = Column(String(255))
    UniqueID = Column(String(255), primary_key=True)
    CycleNumber = Column(Integer, nullable=False)
    Position = Column(String(255), nullable=False)
    EnergySupply = Column(Integer, nullable=False)
    Direction = Column(String(255), nullable=False)
    Age = Column(Integer, nullable=False)

    def __init__(self,
                 SimulationID,
                 UniqueID,
                 CycleNumber,
                 Position,
                 EnergySupply,
                 Direction,
                 Age):

        self.SimulationID = SimulationID
        self.UniqueID = UniqueID
        self.CycleNumber = CycleNumber
        self.Position = Position
        self.EnergySupply = EnergySupply
        self.Direction = Direction
        self.Age = Age


class SimulationLogs(Base):

    __tablename__ = "SimulationLogs"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    SimulationID = Column(String(255), nullable=False)
    Scope = Column(String(255), nullable=False)
    UniqueID = Column(String(255), nullable=False)
    CycleNumber = Column(Integer, nullable=False)
    Granularity = Column(String(255), nullable=False)
    Message = Column(Text, nullable=False)
    Timestamp = Column(String(255), nullable=False)

    def __init__(self,
                 SimulationID,
                 Scope,
                 UniqueID,
                 CycleNumber,
                 Granularity,
                 Message,
                 Timestamp):

        self.SimulationID = SimulationID
        self.Scope = Scope
        self.UniqueID = UniqueID
        self.CycleNumber = CycleNumber
        self.Granularity = Granularity
        self.Message = Message
        self.Timestamp = Timestamp
