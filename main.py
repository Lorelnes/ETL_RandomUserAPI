from constants import URL, create_table_query
from extract import extract_one_user, extract_all_users
from dataclasses import dataclass
from typing import List, Dict
from geopy.geocoders import Nominatim
from pydantic import BaseModel, EmailStr
from transform import *
import pandas as pd
import requests
import logging
from phonenumbers import geocoder
from load import *

# Extraction part

# Calling function for extracting one user
df = pd.DataFrame(extracted_users)

# Transformation part

df = full_name(df)
df['location'] = df.apply(get_location, axis=1)
df['initials'] = df['name'].apply(initials)
df = parsing_phoneloc(df)
df = validate_emails(df)
df = dob_to_datetime(df)
df = reg_to_datetime(df)
df = age_dob(df)
df = age_user(df)
df = drop_some_cols(df)
df = reorder_cols(df)
print(df.columns)

# Loading part
filename = 'all_data.json'
load_to_raw_data(extracted_users)

conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", port='5432')
create_table(conn)
load_data_to_database(df, dbname, user, host, password, port)
