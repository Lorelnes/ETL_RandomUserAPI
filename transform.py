from phonenumbers.phonenumberutil import NumberParseException
from typing import List, Dict, Optional, Any
from geopy.geocoders import Nominatim
from pydantic import BaseModel, EmailStr
from constants import columns_to_drop, columns_to_reorder
from datetime import datetime
import pandas as pd
import phonenumbers


def get_full_name(user_data: Dict[str, Any]) -> Optional[str]:
    '''
    This function takes 'first' and 'last' keys from 'name' dictionary and puts them together to replace
    'name' dictionary with first name and last name.
    '''
    name_data = user_data.get('name', {})
    first_name = name_data.get('first')
    last_name = name_data.get('last')
    if not first_name or not last_name:
        return None
    user_data['name'] = first_name + ' ' + last_name
    return first_name, last_name


def get_location(user_data: Dict[str, Any]) -> Optional[str]:
    '''
    This function extracts latitude and longitude from the 'coordinates' nested dictionary
    in the 'location' dictionary.
    Dynamically finds location using those coordinates.
    '''
    location_data = user_data.get('location', {})
    coordinates = location_data.get('coordinates')
    latitude = coordinates.get('latitude')
    longitude = coordinates.get('longitude')
    if not latitude or not longitude:
        return None
    geolocator = Nominatim(user_agent='geoapieExercises', timeout=20)
    both_coordinates = f'{latitude},{longitude}'
    dynamic_location = geolocator.geocode(both_coordinates)
    user_data['location'] = dynamic_location
    return latitude, longitude


def create_initials_column(user_data: Dict[str, Any]) -> Optional[str]:
    '''
    This function generates initials based on 'name' dictionary and creates separate dictionary to store those initials.
    '''
    name = user_data.get('name')
    init = ""
    for n in name.split():
        init+=n[0]
    user_data['initials'] = init
    return init


def parsing_phone_numbers(user_data: Dict[str, Any]) -> Optional[str]:
    '''
    Creates 'phoneloc' column with phone numbers in E164 format.
    '''
    phone_location = user_data.get('phone') + ' , ' + user_data.get('nat')
    try:
        phone_number = phonenumbers.parse(phone_location, None)
        user_data['phone'] = phone_number
        return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
    except NumberParseException:
        return None


class UserEmail(BaseModel):
    email: EmailStr

def validate_emails(user_data: Dict[str, Any]) -> Optional[str]:
    try:
        validated_email = UserEmail(email=user_data.get('email'))
        user_data['email'] = validated_email.email
        return user_data
    except ValidationError as e:
        logging.error(f'Validation error: {e}')
        return None


def dateofbirth_to_datetime(user_data: Dict[str, Any]) -> Optional[str]:
    '''
    This function formats 'dob' dictionary as datetime and creates another dictionary 'date_of_birth', which contains
    users' date of birth in a more human readable format.
    '''
    dateofbirth = user_data.get('dob')
    date_only = dateofbirth.get('date')
    date_formatted = datetime.strptime(date_only, '%Y-%m-%dT%H:%M:%S.%fZ').date()
    user_data['date_of_birth'] = date_formatted.strftime('%B %d, %Y')
    return user_data


# def registration_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
#     '''
#     This function formats 'registered' column as datetime and creates another column 'registration_date'.
#     '''
#     df['registration_date'] = df['registered'].apply(lambda x: pd.to_datetime(x['date']))
#     return df
#
# def calculate_user_age(df: pd.DataFrame) -> pd.DataFrame:
#     '''
#     This function takes 'date' key from 'dob' column and dynamically calculates the age of the user,
#     then creates 'age' column separately.
#     '''
#
#     today = pd.Timestamp.today().year
#     df['dob'] = df['dob'].apply(lambda x: pd.to_datetime(x['date']))
#     df['age'] = today - df['dob'].dt.year
#     return df
#
# def calculate_registration_age(df: pd.DataFrame) -> pd.DataFrame:
#     '''
#     This function takes 'age' key from 'registered' column and dynamically calculates the registration age of the user,
#     then creates 'age_as_user' column separately.
#     '''
#     today = pd.Timestamp.today().year
#     df['registered'] = df['registered'].apply(lambda x: pd.to_datetime(x['date']))
#     df['age_as_user'] = today - df['registered'].dt.year
#     return df
#
#
# def drop_unnecessary_columns(df: pd.DataFrame) -> pd.DataFrame:
#     '''
#     This function deletes columns that are not needed.
#     '''
#     df = df.drop([columns_to_drop])
#     return df
#
# def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
#     '''
#     This function reorders columns in a more logical way.
#     '''
#
#     return df[columns_to_reorder]













