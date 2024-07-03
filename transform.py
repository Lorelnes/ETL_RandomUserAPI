from constants import URL # unused
from phonenumbers import geocoder # unused
from phonenumbers.phonenumberutil import NumberParseException
from dataclasses import dataclass, field # unused import
from typing import List, Dict, Optional
from geopy.geocoders import Nominatim
from pydantic import BaseModel, EmailStr
import pandas as pd
import datetime # unused
import phonenumbers
import time # unused


def full_name(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function takes 'first' and 'last' keys from 'name' dict and puts them together to replace
    'name' column with first name and last name.
    '''
    df['name'] = df['name'].apply(lambda x: f"{x.get('first', '')} {x.get('last', '')}")
    return df

def get_location(row: Dict) -> Optional[str]:
    # what is row and where did it come from
    # it would be optional if you pass lan and lon as arguments to the function and return the plance
    # later this function can be used to apply it on a df
    '''
    This function extracts latitude and longitude from the 'coordinates' dictionary
    in the 'location' column.
    Dynamically finds location using those coordinates.

    Args:
        row: A dictionary containing the extracted data.

    Returns:
        Location which is a string containing detailed location information or None if
        the location is not found.
    '''

    location_data = row['location']
    latitude = location_data.get('coordinates', {}).get('latitude')
    longitude = location_data.get('coordinates', {}).get('longitude')

    # this expression can be simplified
    if latitude is None and longitude is None:
        return None
    
    # if latitude and longitude
        # geolocator =Nominatim(user_agent='geoapieExercises', timeout=20)
        # coordinates = f"{latitude},{longitude}"
        # Location = geolocator.geocode(coordinates)

        # return Location
    # return None

    geolocator =Nominatim(user_agent='geoapieExercises', timeout=20)
    coordinates = f"{latitude},{longitude}"
    Location = geolocator.geocode(coordinates)

    return Location


# functions name is not clear, will confuse other developers
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


def format_phone_number(phoneloc_str: str) -> Optional[str]:
    '''
    Parses and formats a phone number string in E164 format.

    Args:
        phoneloc_str: A string containing phone number and nationality.

    Returns:
        The parsed phone number in E164 format (or None if parsing fails).
    '''
    try:
        phnumber = phonenumbers.parse(phoneloc_str, None)
        return phonenumbers.format_number(phnumber, phonenumbers.PhoneNumberFormat.E164)
    except NumberParseException:
        return None

def parsing_phoneloc(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Creates 'phoneloc' column with phone numbers in E164 format.

    Args:
        df: Pandas DataFrame containing 'phone' and 'nat' columns.

    Returns:
        The modified DataFrame with the 'phoneloc' column.
    '''
    df['phoneloc'] = df[['phone', 'nat']].apply(lambda x: f"{x['phone']}, {x['nat']}", axis=1)
    df['phoneloc'] = df['phoneloc'].apply(format_phone_number) 
    return df


def validate_emails(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function is used to create Pydantic class to validate emails.

    Args: df

    Returns: df
    '''
    #  returns df, args df says nothing. if there is no good information better to remove them

    # this class is defined inside a function and you are not even using it
    # I do not see a reason why you should be definind a class inside a function, even more a dataclass
    # if you want to validate your data, create a class outside of a function and use it.
    class UserEmail(BaseModel):
        email: EmailStr

    emails = df['email'].tolist()
    for email in emails:
        try:
            #  you are validating the user email and then just returning same email, how is that going to work?
            validated_user = UserEmail(email=email)
        except pydantic.ValidationError as e:
            # log the error, do not print it
            print(f'Validation Error: {e}')
    return df


def dob_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function formats 'dob' column as datetime and creates another column 'date_of_birth'.
    '''
    df['date_of_birth'] = df['dob'].apply(lambda x: pd.to_datetime(x['date']))
    return df

def reg_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function formats 'registered' column as datetime and creates another column 'registration_date'.
    '''
    df['registration_date'] = df['registered'].apply(lambda x: pd.to_datetime(x['date']))
    return df

def age_dob(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function takes 'date' key from 'dob' column and dynamically calculates the age of the user, then creates 'age' column separately.
    '''

    today = pd.Timestamp.today().year
    df['dob'] = df['dob'].apply(lambda x: pd.to_datetime(x['date']))
    df['age'] = today - df['dob'].dt.year
    return df

def age_user(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function takes 'age' key from 'registered' column and dynamically calculates the registration age of the user,
    then creates 'age_as_user' column separately.
    '''
    today = pd.Timestamp.today().year
    df['registered'] = df['registered'].apply(lambda x: pd.to_datetime(x['date']))
    df['age_as_user'] = today - df['registered'].dt.year
    return df


def drop_some_cols(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function deletes columns that are not needed.

    Args: df

    Returns: df.
    '''
    df = df.drop(columns=['login', 'cell', 'picture', 'dob', 'registered', 'phoneloc', 'id'])
    return df

def reorder_cols(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function reorders columns in a more logical way.
    Args: df
    Returns: df.
    '''
    #  these are the columns you need, better to have it in the separate file as constants, easier to use
    reordered = ['gender', 'name', 'initials', 'location', 'date_of_birth', 'age', 'registration_date', 'age_as_user',
                 'email', 'phone', 'nat']

    return df[reordered]









