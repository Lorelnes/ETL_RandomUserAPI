from constants import create_table_query, insert_data_query
from transform import df
from settings import dbname, user, host, password, port
import psycopg2
import logging

def check_table_existence(conn, table_name: str):
    """
      Checks if a table with the specified name exists in the connected database.

      Args:
          conn: A psycopg2 connection object to the database.
          table_name: The name of the table to check for existence.

      Returns:
          True if the table exists, False otherwise.
      """
    cur = conn.cursor()
    cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (table_name))
    exists = cur.fetchone()[0]
    cur.close()
    return exists

def table_name_from_schema(conn, table_name: str, schema: dict) -> None:
    """
      Creates a table in the connected database based on the provided schema.

      Args:
          conn: A psycopg2 connection object to the database.
          table_name: The desired name for the created table.
          schema: A dictionary defining the table's columns and their data types.
              Dictionary keys are column names, and values are data types as strings.

      Raises:
          Exception: If the table creation fails.
      """
    try:
        columns = ", ".join(f"{column_name} {data_type}" for column_name, data_type in schema.items())
        cur.execute(f"CREATE TABLE {table_name} ({columns})")
        conn.commit()
    except psycopg2.Error as e:
        logging.error(f"Error creating table '{table_name}': {e}")
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

       df.to_sql(table_name, conn, if_exists='append', index=False)

       conn.commit()

    except psycopg2.Error as e:
        logging.error(f"Error occured during data loading: {e}")
    finally:
            conn.close()
