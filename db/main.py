import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base, CycleResults, SimulationSummary, SimulationLogs, DooderResults

load_dotenv()


class RecordTypes:
    CycleResults = CycleResults
    SimulationSummary = SimulationSummary
    SimulationLogs = SimulationLogs
    DooderResults = DooderResults

    @classmethod
    def get(cls, record_type):
        return getattr(cls, record_type)


class DB:

    def __init__(self):
        self.base = Base
        self.engine = self.create_engine()
        self.session = sessionmaker(bind=self.engine)()

    def create_engine(self):
        host = os.environ.get("POSTGRES_HOST")
        database = os.environ.get("POSTGRES_DB")
        user = os.environ.get("POSTGRES_USER")
        password = os.environ.get("POSTGRES_PASSWORD")
        engine = create_engine(
            f"postgresql+psycopg2://{user}:{password}@{host}:5432/{database}")

        return engine

    def df_to_db(self, df, record_type):
        # maybe have a decorator that creates and closes a session
        df_dict = df.to_dict('rows')

        self.session = self.create_session()

        for record in df_dict.values():
            self.add_record(record, record_type)

        self.session.commit()
        self.session.close()

    def add_record(self, record: dict, record_type: str):
        # have class that when init it returns a desired result. like a vending machine. This class sacrifices itself. send a class and do something based on the type of class. basically encoding then decoding
        serializer = RecordTypes.get(record_type)
        serialized_record = serializer(**record)
        self.session.add(serialized_record)

    def add(self, record: dict, record_type: str):
        self.session = self.create_session()
        self.add_record(record, record_type)
        
        self.session.commit()
        self.session.close()

    def reset(self):
        self.tear_down()
        self.build_up()
        print("DB reset successfully")

    def build_up(self):
        self.base.metadata.create_all(self.engine)
        print("DB Tables created")

    def tear_down(self):
        self.base.metadata.drop_all(self.engine)
        print("DB Tables dropped")
