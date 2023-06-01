"""
Information Model
-----------------
Information component used to collect data from the simulation.
This class provides the prim ary capability to collect data from the
simulation at the end of each cycle. The data is stored in a dictionary
named 'data'.

Collectors are the registered functions that are used to collect specific data.
All collectors are stored in the collectors attribute. The collectors attribute
is a dictionary of dictionaries. The first key is the collector component.

This component is also the main method to log activity from the simulation.
All activity is logged to a file based on specified granularity. Granularity
is defined as the level of detail to log. 1 is the lowest and most important
level of detail. 3 is the highest and most detailed level of detail, including
when energy dissipation occurs, failed movements, and failed actions, etc..
"""

import sqlite3
import traceback
from typing import TYPE_CHECKING, List

import pandas as pd

from dooders.sdk.utils.logger import get_logger

if TYPE_CHECKING:
    from dooders.sdk.simulation import Simulation


class FakeLogger:

    def info(self, message: str) -> None:
        pass

    def log(self, message: str, granularity: int) -> None:
        pass


class Information:
    """
    Class for collecting data from the simulation.

    Parameters
    ----------
    simulation_id: str
        The unique ID for the simulation.

    Attributes
    ----------
    simulation_id: see Parameters
    logger: Logger
        Logger that handles all logging for the simulation.
    granularity: int
        Higher granularity means more detailed logging.

    Methods
    -------
    collect(simulation: 'Simulation') -> None
        Collect data from the simulation.
    post_collect() -> None
        Process taking place after data collection.
    get_result_dict(simulation: 'Simulation') -> dict
        Get a dictionary of the results of the experiment.
    clear() -> None
        Clear the data dictionary but keep the structure.
    reset() -> None
        Reset the information component in case the simulation restarts.
    store() -> None
        Store the data in the database.
    """

    data: dict = {}

    @classmethod
    def _init_information(cls, simulation: 'Simulation') -> None:
        cls.logger = FakeLogger()  # ! remove this from the class
        cls.granularity = 2
        cls.simulation_id = simulation.simulation_id
        cls.batch_process = simulation.batch_process

        # with sqlite3.connect("recent/Simulation.db") as conn:
        #     cls._delete_existing_tables(conn)

    @classmethod
    def collect(cls, simulation: 'Simulation') -> None:
        """
        Collect data from the simulation.

        Parameters
        ----------
        simulation: Object
            Data is collected from the simulation object.
        """
        models = ['arena', 'resources']
        try:
            cls_data = cls.data
            for model_name in models:
                model = getattr(simulation, model_name)
                model_data = model.collect()
                model_data_store = cls_data.setdefault(model_name, {})
                for key, value in model_data.items():
                    model_data_store.setdefault(key, []).append(value)

            if simulation.cycle_number % 1000 == 0:
                if cls.batch_process:
                    # cls.store()
                    pass
                cls.data = cls.clear()

        except Exception as e:
            print(traceback.format_exc())

    @classmethod
    def log(cls, message: str, granularity: int) -> None:
        """
        Log a message.

        Parameters
        ----------
        message: str
            The message to log.
        granularity: int
            The granularity of the message.
        """
        if granularity <= cls.granularity:
            message_string = f"'SimulationID':'{cls.simulation_id}', {message}"

            cls.logger.info(message_string)

    @classmethod
    def reset(cls) -> None:
        """
        Reset the information component in case the simulation restarts
        """
        cls.data = {}

    @classmethod
    def clear(cls) -> None:
        """ 
        Recursively clear the data dictionary on the last key: value pair.

        This method is used to clear the data dictionary after the data has been
        collected. 

        This is done to prevent the data object from growing exponentially
        """
        data = cls.data.copy()
        stack = [(data, 0, list(data.keys()))]

        while stack:
            current_dict, depth, keys = stack[-1]

            if keys:
                key = keys.pop()
                value = current_dict[key]

                if isinstance(value, dict):
                    stack.append((value, depth + 1, list(value.keys())))
                elif isinstance(value, list):
                    current_dict[key] = []
                else:
                    current_dict[key] = None
            else:
                stack.pop()

        return data

    @classmethod
    def store(cls) -> None:
        """
        Store the data in the database.
        """
        with sqlite3.connect("recent/Simulation.db") as conn:
            cls._create_table_and_insert_data(conn)
            conn.commit()

    @classmethod
    def _delete_existing_tables(cls, conn: sqlite3.Connection) -> None:
        """ 
        Delete all existing tables in the database.

        Parameters
        ----------
        conn: sqlite3.Connection
            Connection to the database.
        """
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        for table_name in tables:
            conn.execute(f"DROP TABLE {table_name[0]}")

    @classmethod
    def _create_table_and_insert_data(cls, conn: sqlite3.Connection) -> None:
        """ 
        Create a table for each model and insert the data into the table.

        Parameters
        ----------
        conn: sqlite3.Connection
            Connection to the database.
        """

        for table_name, columns in cls.data.items():
            # Get unique column names
            column_names = list(columns.keys())

            # Replace parentheses with underscores for column names
            formatted_column_names = [col_name.replace(
                '(', '_').replace(')', '') for col_name in column_names]

            # Dynamically create table
            column_definitions = ", ".join(
                [f"{col_name} REAL" for col_name in formatted_column_names])
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})"
            conn.execute(create_table_query)

            # Insert data into the table
            placeholders = ", ".join(["?" for _ in formatted_column_names])
            insert_data_query = f"INSERT INTO {table_name} ({', '.join(formatted_column_names)}) VALUES ({placeholders})"

            for row in zip(*columns.values()):
                conn.execute(insert_data_query, row)
