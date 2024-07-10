from phonenumbers.phonenumberutil import NumberParseException
from typing import List, Dict, Optional, Any
from geopy.geocoders import Nominatim
from pydantic import BaseModel, EmailStr
from constants import columns_to_drop, columns_to_reorder
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


# def parsing_phoneloc(df: pd.DataFrame) -> pd.DataFrame:
#     '''
#     Creates 'phoneloc' column with phone numbers in E164 format.
#
#     Args:
#         df: Pandas DataFrame containing 'phone' and 'nat' columns.
#
#     Returns:
#         The modified DataFrame with the 'phoneloc' column.
#     '''
#     df['phoneloc'] = df[['phone', 'nat']].apply(lambda x: f"{x['phone']}, {x['nat']}", axis=1)
#
#     # Apply format_phone_number function to each element in 'phoneloc' column
#     df['phoneloc'] = df['phoneloc'].apply(format_phone_number)
#     return df
#
#
# def format_phone_number(phoneloc_str: str) -> Optional[str]:
#     '''
#     Parses and formats a phone number string in E164 format.
#
#     Args:
#         phoneloc_str: A string containing phone number and nationality.
#
#     Returns:
#         The parsed phone number in E164 format (or None if parsing fails).
#     '''
#     try:
#         phnumber = phonenumbers.parse(phoneloc_str, None)
#         return phonenumbers.format_number(phnumber, phonenumbers.PhoneNumberFormat.E164)
#     except phonenumbers.NumberParseException:
#         return None
#
#
# def validate_emails(df: pd.DataFrame) -> pd.DataFrame:
#     '''
#     This function is used to create Pydantic class to validate emails.
#     '''
#     # this class is defined inside a function and you are not even using it
#     # I do not see a reason why you should be definind a class inside a function, even more a dataclass
#     # if you want to validate your data, create a class outside of a function and use it.
#     class UserEmail(BaseModel):
#         email: EmailStr
#
#     emails = df['email'].tolist()
#     for email in emails:
#         try:
#             #  you are validating the user email and then just returning same email, how is that going to work?
#             validated_user = UserEmail(email=email)
#         except pydantic.ValidationError as e:
#             # log the error, do not print it
#             logging.error(f'Validation Error {e}')
#     return df
#
#
# def dateofbirth_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
#     '''
#     This function formats 'dob' column as datetime and creates another column 'date_of_birth'.
#     '''
#     df['date_of_birth'] = df['dob'].apply(lambda x: pd.to_datetime(x['date']))
#     return df
#
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













