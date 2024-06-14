from constants import URL, HEADERS
from extract import RandomUserAPI
from transform import *
from settings import *
import pandas as pd
import requests
import json

# Extraction part

# Initializing RandomUserAPI object
api = RandomUserAPI()

# Extracting user data
all_data = api.extract_all_data()

# Saving data to JSON and in raw_data directory
api.save_to_json(all_data, directory=raw_data, filename="all_data.json")

# Transformation part

# Calling functions from transform.py
dob_to_datetime(df, 'dob.date')
registered_to_datetime(df, 'registered.date')
dob_age(df, 'dob.date')
registered_age(df, 'registered.date')


# Loading part
load_data_to_database(df, dbname, user, host, password, port)


