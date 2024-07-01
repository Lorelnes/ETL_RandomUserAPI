from constants import create_table_query, insert_data_query
from extract import *
from settings import dbname, user, host, password, port
from psycopg2.extras import execute_values
import pandas as pd
import psycopg2
import logging
import os
import json
def load_to_raw_data(data: list, filename: str = 'all_data.json') -> None:
    raw_data_dir = 'raw_data'
    filepath = os.path.join(raw_data_dir, filename)

    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent = 4)
        logging.info(f'Data was saved to {filepath}')

def create_table(conn) -> None:
    """
      Creates a table in the connected database based on the provided schema.

      Args:
          conn: A psycopg2 connection object to the database.

      """
    try:
        cur = conn.cursor()
        cur.execute(create_table_query)
        conn.commit()
        logging.info(f'Table was created')
    except psycopg2.Error as e:
        logging.error(f"Error creating table: {e}")
    finally:
        cur.close()

def load_data_to_database(df: pd.DataFrame, dbname: str, user: str, host: str, password: str, port: int) -> None:
    """
     Loads data from a pandas DataFrame into a table in the specified database.

     Args:
         df: The pandas DataFrame containing the data to be loaded.
         dbname: The name of the database.
         user: The username for database access.
         host: The hostname or IP address of the database server.
         password: The password for database access.
         port: The port number of the database server.

     Raises:
         psycopg2.Error: If an error occurs during database connection or data loading.
     """
    try:
       conn = psycopg2.connect(dbname=dbname, user=user, host=host, password=password, port=port)

       cur = conn.cursor()

       cur.executemany(insert_data_query, df.values.tolist())

       conn.commit()

       logging.info(f'Data was loaded to database')

    except psycopg2.Error as e:
        logging.error(f"Error occured during data loading: {e}")
    finally:
        conn.close()
