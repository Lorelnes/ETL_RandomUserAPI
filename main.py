from constants import URL
from extract import extract_one_user
from dataclasses import dataclass
from typing import List, Dict
from geopy.geocoders import Nominatim
import pandas as pd
import requests
import logging

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
    latitude = [row.get('coordinates', {}).get('latitude') for row in df['location']]
    longitude = [row.get('coordinates', {}).get('longitude') for row in df['location']]
    if latitude is None and longitude is None:
        return None

    for lan, lon in zip(latitude, longitude):
        coordinates = f"{lan},{lon}"
        Location = geolocator.geocode(coordinates)

get_location(df)

df['location'] = df['location'].apply(get_location)

# Creating new column containing user initials and moving it after 'name' column
def initials(name):
    init = ""
    for n in name.split():
        init+=n[0]
    return init
df['initials'] = df['name'].apply(initials)

column_names = list(df.columns)
name_index = column_names.index('name')
column_names.insert(name_index + 1, column_names.pop(column_names.index('initials')))
df = df[column_names]




