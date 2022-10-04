"""

#! function to drop table if exists, compile table from incoming data, create new table
"""

import psycopg2
import psycopg2.extras as extras
from pydantic import BaseModel


class PostgresData(BaseModel):
    ExperimentID: str
    CycleNumber: int
    DooderCount: int
    EnergyCount: int
    TotalDooderEnergySupply: int
    AverageEnergyAge: float


def create_connection():
    """

    """
    # Connect to the database
    conn = psycopg2.connect(
        host="192.168.1.220",
        database="DooderDB",
        user="postgres",
        password="changeme"
    )

    return conn


def execute_query(query: str, params={}) -> None:
    """Execute a query."""
    conn = create_connection()
    # Create a cursor
    cur = conn.cursor()

    # Execute the query
    cur.execute(query, params)

    # Commit the changes to the database
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()


def upload_results(cycle_results: dict) -> None:
    """Upload the results to the postgres server."""

    final_results = PostgresData.construct(**cycle_results).dict()

    # Create a new record
    sql = """
    INSERT INTO public."SimulationResults" ("ExperimentID", "CycleNumber", "DooderCount", "EnergyCount", "TotalDooderEnergySupply", "AverageEnergyAge") 
    VALUES (%(ExperimentID)s, %(CycleNumber)s, %(DooderCount)s, %(EnergyCount)s, %(TotalDooderEnergySupply)s, %(AverageEnergyAge)s);
    """

    execute_query(sql, final_results)


def clear_table(table_name: str) -> None:
    """Clear the table of all data."""

    # Clear the table
    sql = f"""
    DELETE FROM public."{table_name}";
    """.format(table_name)

    execute_query(sql)


def df_to_db(df, table_name: str) -> None:

    conn = create_connection()
    columns = [col for col in df.columns if col in COLUMNS[table_name]]
    cols = ', '.join(f'"{w}"' for w in columns)
    final_df = df[columns]
    tuples = [tuple(x) for x in final_df.to_numpy()]
    table = f"""public."{table_name}" """
    query = """INSERT INTO %s(%s) VALUES %%s""" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    cursor.close()


COLUMNS = {
    'DooderResults': [
        'CycleNumber',
        'UniqueID',
        'Position',
        'EnergySupply',
        'Age',
        'Direction'],
    'SimulationResults': [
        'ExperimentID',
        'CycleNumber',
        'DooderCount',
        'EnergyCount',
        'TotalDooderEnergySupply',
        'AverageEnergyAge'],
    'SimulationLogs': [
        'timestamp',
        'experiment_id',
        'scope',
        'id',
        'cycle_number',
        'granularity',
        'message'
        ]
}
