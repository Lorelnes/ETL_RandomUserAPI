from constants import create_table_query, insert_data_query
from extract import extract_one_user
from settings import dbname, user, host, password, port
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

def create_table(conn, create_table_query) -> None:
    """
      Creates a table in the connected database based on the provided schema.

      Args:
          conn: A psycopg2 connection object to the database.
          create_table_query: A psycopg2 query to create the table.
      """
    try:
        cur = conn.cursor()
        cur.execute(create_table_query)
        conn.commit()
        logging.info(f'Table was created')
    except psycopg2.Error as e:
        logging.error(f"Error creating table: {e}")

def load_data_to_database(user_data: Dict, conn) -> None:
    """
     Loads data into a table in the specified database.
    """
    try:
       cur = conn.cursor()

       cur.executemany(insert_data_query, [user_data])

       conn.commit()

       logging.info(f'Data was loaded to database')

    except psycopg2.Error as e:
        logging.error(f"Error occured during data loading: {e}")

