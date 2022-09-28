from pydantic import BaseModel
import psycopg2


class PostgresData(BaseModel):
    ExperimentID: str
    CycleNumber: int
    DooderCount: int
    EnergyCount: int
    TotalDooderEnergySupply: int
    AverageEnergyAge: float

def upload_results(cycle_results: dict) -> None:
    """Upload the results to the postgres server."""
    
    final_results = PostgresData.construct(**cycle_results).dict()

    # Connect to the database
    conn = psycopg2.connect(
        host="192.168.1.220",
        database="DooderDB",
        user="postgres",
        password="changeme"
        )

    # Create a cursor
    cur = conn.cursor()

    # Create a new record
    sql = """
    INSERT INTO public."SimulationResults" ("ExperimentID", "CycleNumber", "DooderCount", "EnergyCount", "TotalDooderEnergySupply", "AverageEnergyAge") 
    VALUES (%(ExperimentID)s, %(CycleNumber)s, %(DooderCount)s, %(EnergyCount)s, %(TotalDooderEnergySupply)s, %(AverageEnergyAge)s);
    """
    cur.execute(sql, final_results)

    # Commit the changes to the database
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()
