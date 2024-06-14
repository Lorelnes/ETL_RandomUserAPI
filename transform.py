from main import all_data
from extract import *
import pandas as pd
import datetime

df = pd.DataFrame(all_data)
def dob_to_datetime(df: pd.DataFrame, dob: str) -> None:
  """
  Transforms the specified 'dob' column in the DataFrame to datetime format.

  Args:
      df: The DataFrame containing the dob column.
      dob: The name of the column containing date strings.
  """
  df['dob.datetime'] = pd.to_datetime(df['dob.date'])

def registered_to_datetime(df: pd.DataFrame, registered: str) -> None:
    """
     Transforms the specified 'registered' column in the DataFrame to datetime format.

     Args:
         df: The DataFrame containing the registered column.
         registered: The name of the column containing date strings.
     """
    df['registered.datetime'] = pd.to_datetime(df['registered.date'])


def dob_age(df: pd.DataFrame, dob: str) -> None:
    """
      Calculates the age dynamically based on the specified 'dob' column and modifies the DataFrame in-place.

      Args:
          df: The DataFrame containing the 'dob' column.
          dob: The name of the column containing date of birth information.
      """
    today = pd.Timestamp.today()
    df['age'] = today.year - pd.to_datetime(df[dob.date]).year

def registered_age(df: pd.DataFrame, registered: str) -> None:
    """
      Calculates the age dynamically based on the specified 'registered' column and modifies the DataFrame in-place.

      Args:
          df: The DataFrame containing the 'registered' column.
          registered: The name of the column containing date of registration information.
      """
    today = pd.Timestamp.today()
    df['age'] = today.year - pd.to_datetime(df[registered]).year