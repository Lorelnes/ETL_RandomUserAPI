import phonenumbers

from constants import URL
from extract import extract_one_user
from dataclasses import dataclass
from typing import List, Dict
from geopy.geocoders import Nominatim
from pydantic import BaseModel, EmailStr
import pandas as pd
import requests
import logging
from phonenumbers import geocoder

# Extraction part

# Calling function for extracting one user
one_user = extract_one_user(URL)

def extract_all_users(URL: str) -> List[dict]:
    """
    Extracts 1000 user data from the URL and returns dictionary:

    Args:
         URL(type hint: str) : the URL from which we extract the data.

    Returns:
         dict: A dictionary containing the extracted data.

    Logs:
         INFO: logs the number of extracted users.
         WARNING: logs a message if we already extracted 1000 users.
    """
    extracted_users = []
    for i in range(5):
        user = extract_one_user(URL)
        if user:
            extracted_users.append(user)
            if extracted_users:
                logging.info(f"Extracted {len(extracted_users)} users")
            else:
                logging.warning("No users extracted")

    return extracted_users

extracted_users = extract_all_users(URL)

# Transformation part

# Turning data into dataframe
df = pd.DataFrame(extracted_users)

# Normalizing column 'name'
df['name'] = df['name'].apply(lambda x: f"{x.get('first', '')} {x.get('last', '')}")


# Dynamically generating location based on coordinates
geolocator = Nominatim(user_agent='geoapieExercises', timeout=10)
def get_location(row):
    '''
    This function extracts latitude and longitude from the 'coordinates' dictionary
    in the 'location' column.
    Dynamically finds location using those coordinates.

    Args:
        row: A dictionary containing the extracted data.

    Returns:
        Location which is a string containing detailed location information.
    '''
    latitude = [row.get('coordinates', {}).get('latitude') for row in df['location']]
    longitude = [row.get('coordinates', {}).get('longitude') for row in df['location']]
    if latitude is None and longitude is None:
        return None

    for lat, lon in zip(latitude, longitude):
        coordinates = f"{lat},{lon}"
        Location = geolocator.geocode(coordinates)

get_location(df)

df['location'] = df['location'].apply(get_location)

# Creating new column containing user initials and moving it after 'name' column
def initials(name: str) -> str:
    '''
    This function generates initials based on 'name' column.

    Args:
        name: column containing names and lastnames of users.

    Returns:
        A string containing initials for users' full names.
    '''
    init = ""
    for n in name.split():
        init+=n[0]
    return init
df['initials'] = df['name'].apply(initials)

column_names = list(df.columns)
name_index = column_names.index('name')
column_names.insert(name_index + 1, column_names.pop(column_names.index('initials')))
df = df[column_names]
# Formatting phone numbers in E164

df['phoneloc'] = df['phone'] + ', ' + df['nat']
def parsing_phoneloc(phoneloc: pd.Series) -> pd.Series:
    """
    Based on 'phoneloc' column we defined above by joining 'phone' and 'nat' columns,
    this function creates E164 formatting for phone numbers.

    Args:
        phoneloc: Pandas series containing strings which represent phone number and nationality.

    Returns:
        Pandas series containing parsed phone numbers in E164 format.
    """
    phnumber = phonenumbers.parse(phoneloc, 'US')
    return phonenumbers.format_number(phnumber, phonenumbers.PhoneNumberFormat.E164)

df['phone'] = df['phone'].apply(parsing_phoneloc)
df = df.drop(columns=['phoneloc'])

# Validating email with pydantic
class UserEmail(BaseModel):
    email: EmailStr

df_to_dict = df.to_dict(orient='records')

valid_data = []
for i in df_to_dict:
    valid_data.append(i)

df = pd.DataFrame(valid_data)

# Formatting dob as datetime and renaming it 'date_of_birth'
df['date_of_birth'] = df['dob'].apply(lambda x: pd.to_datetime(x['date']))

# Formatting registered as datetime and renaming it 'registration_date'
df['registration_date'] = df['registered'].apply(lambda x: pd.to_datetime(x['date']))

# Dynamically calculating age based on date_of_birth, removing 'age' key from 'dob' column, making it a separate column, then dropping 'dob' column altogether
df['dob'] = df['dob'].apply(lambda x: pd.to_datetime(x['date']))
today = pd.Timestamp.today().year
df['age'] = today - df['dob'].dt.year
df = df.drop(columns=['dob'])

# Dynamically calculating age as a user based on registration_date, making age_as_user separate column, dropping 'registered' column
df['registered'] = df['registered'].apply(lambda x: pd.to_datetime(x['date']))
df['age_as_user'] = today - df['registered'].dt.year
df = df.drop(columns=['registered'])

# Dropping unnecessary columns
df = df.drop(columns=['login', 'cell', 'picture'])

# Reordering the columns
reordered = ['gender', 'name', 'initials', 'location', 'date_of_birth', 'age', 'registration_date', 'age_as_user', 'email', 'phone', 'id', 'nat']
df = df[reordered]

