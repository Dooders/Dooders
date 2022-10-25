import os

import psycopg2
import psycopg2.extras as extras
from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import create_engine
engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')
postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]


class DBConnect:

    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.environ.get("POSTGRES_HOST"),
            database=os.environ.get("POSTGRES_DB"),
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
        )
        self.cur = self.conn.cursor()

    def execute_query(self, query: str, params={}):
        self.cur.execute(query, params)
        self.conn.commit()

    def df_to_db(self, df, table_name: str) -> None:
        columns = [col for col in df.columns if col in COLUMNS[table_name]]
        cols = ', '.join(f'"{w}"' for w in columns)
        final_df = df[columns]
        tuples = [tuple(x) for x in final_df.to_numpy()]
        table = f"""public."{table_name}" """
        query = """INSERT INTO %s(%s) VALUES %%s""" % (table, cols)

        try:
            extras.execute_values(self.cur, query, tuples)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn.rollback()
            self.cur.close()
            return 1

        self.cur.close()

    def close(self):
        self.cur.close()
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()
