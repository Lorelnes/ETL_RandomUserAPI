from constants import URL, create_table_query, table_schema
from extract import extract_one_user # unused
from dataclasses import dataclass # unused
from typing import List, Dict # unused
from geopy.geocoders import Nominatim # unused
from pydantic import BaseModel, EmailStr # unused
from load import load_to_raw_data, create_table, load_data_to_database
from transform import get_full_name, get_location, create_initials_column, parsing_phone_numbers
from settings import dbname, user, host, password, port
from phonenumbers import geocoder # unused
from psycopg2 import sql
import pandas as pd
import requests # unused
import logging # unused
import json


# GENERAL COMMENCTS ABOUT THE PROGRAM
"""


++++++++++++++++++++++++++++ FUTURE CONSIDERATIONS ++++++++++++++++++++++++++++
7. when working on a project, good to have requirements.txt file, please look it up. when you use any kind of third party library
I have to install it when cloning your directory. better to have all of them in requirements. basically when you begin create .venv
and when you are done freeze the requirements. one of the ways is to execute following command:
    pip freeze > requirements.txt

8. we should start working more with git, when you are making some initial development, create a branch, work there, and then
create a pull request for me to review and approve. try watching videos from syllabus or read material about branching strategies.
"""

user_data = extract_one_user(URL)
get_full_name(user_data)
get_location(user_data)
create_initials_column(user_data)
parsing_phone_numbers(user_data)

print(user_data)

# Extraction part
# extracted_users = extract_all_users(URL)

# Calling function for extracting one user
# df = pd.DataFrame(extracted_users)
#
# # Transformation part
# get_full_name(df)
# print(df.columns)
# df['location'] = df.apply(get_location, axis=1)
# print(df.columns)
#
# df['initials'] = df['name'].apply(create_initials_column)
# df = parsing_phoneloc(df)
# df = format_phone_number(df)
# print(df.columns)
# df = (df.pipe(validate_emails).pipe(dateofbirth_to_datetime).pipe(registration_to_datetime).pipe(calculate_user_age).pipe(calculate_registration_age).pipe(drop_unnecessary_columns).pipe(reorder_columns))
#
#
# # Loading part
# load_to_raw_data(extracted_users)
#
# conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
# create_table(conn, create_table_query)
#
# load_data_to_database(df, conn)
# conn.close()
