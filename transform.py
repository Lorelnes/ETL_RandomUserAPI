from extract import extract_one_user
from dataclasses import dataclass, field
from constants import URL
from geopy.geocoders import Nominatim
import pandas as pd
import datetime

@dataclass
class Name:
    first: str
    last: str

@dataclass
class Location:
    latitude: float
    longitude: float
    location: field(init=False)

@dataclass
class User:
    gender: str
    name: Name
    location: Location
    email: str
    dob: datetime
    registered: datetime
    nat: str


geolocator = Nominatim(user_agent='geoapieExercises')


user = extract_one_user(URL)
latitude = user['location']['coordinates']['latitude']
longitude = user['location']['coordinates']['longitude']
print(user)
location = geolocator.geocode(latitude+","+longitude)
print(location)
print(longitude)
print(latitude)