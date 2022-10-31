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

def create_connection():
    host = os.environ.get("POSTGRES_HOST")
    database = os.environ.get("POSTGRES_DB")
    user = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")
    engine = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:5432/{database}")

    return engine

def session(func):
    def wrapper(*args, **kwargs):
        engine = create_connection()
        session = sessionmaker(bind=engine)()
        result = func(*args, session=session, **kwargs)
        session.commit()
        session.close()
        return result

    return wrapper

class DB:
    # refactor to create sessions more efficiently
    
    base = Base

    @classmethod
    def df_to_db(cls, df, record_type):
        # maybe have a decorator that creates and closes a session
        df_list = df.to_dict('records')

        for record in df_list:
            cls.add_record(record, record_type)

    @classmethod
    @session
    def add_record(cls, record: dict, record_type: str, *args, **kwargs):
        session = kwargs.get('session')
        serializer = RecordTypes.get(record_type)
        serialized_record = serializer(**record)
        cls._add(session, serialized_record)
        
    @classmethod
    def _add(cls, session, record):
        session.add(record)

    @classmethod
    def reset(cls):
        cls.engine = create_connection()
        cls.tear_down()
        cls.build_up()
        print("DB reset successfully")

    @classmethod
    def build_up(cls):
        cls.base.metadata.create_all(cls.engine)
        print("DB Tables created")

    @classmethod
    def tear_down(cls):
        cls.base.metadata.drop_all(cls.engine)
        print("DB Tables dropped")
