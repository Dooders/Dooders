import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base

load_dotenv()


class DBAdmin:

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

    def build_up(self):
        self.base.metadata.create_all(self.engine)

    def tear_down(self):
        self.base.metadata.drop_all(self.engine)
