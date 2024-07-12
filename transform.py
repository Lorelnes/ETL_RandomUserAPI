from phonenumbers.phonenumberutil import NumberParseException
from typing import Dict, Optional, Any
from geopy.geocoders import Nominatim
from pydantic import BaseModel, EmailStr
from constants import keys_to_drop, keys_to_reorder
from datetime import datetime
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
    geolocator = Nominatim(user_agent='geoapieExercises', timeout=25)
    both_coordinates = f'{latitude},{longitude}'
    dynamic_location = geolocator.geocode(both_coordinates)
    user_data['location'] = dynamic_location.address if dynamic_location else None
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
    dates_of_birth = user_data.get('dob')
    date_only = dates_of_birth.get('date')
    # date_with_timezone = datetime.strptime(date_only, "%Y-%m-%dT%H:%M:%S.%fZ")
    # date_without_timezone = date_with_timezone.replace(tzinfo=None)
    # date_formatted = date_with_timezone.strftime("%Y-%m-%d")
    # user_data['date_of_birth'] = date_formatted
    date_formatted = date_only.split('T')[0]
    date_formatted = datetime.strptime(date_formatted, "%Y-%m-%d").date().strftime('%Y-%m-%d')
    user_data['date_of_birth'] = date_formatted

    # date_formatted = datetime.strptime(date_only, "%Y-%m-%dT%H:%M:%S.%fZ")
    # date_without_timezone = date_formatted.replace(tzinfo=None)
    # date_into_string = date_without_timezone.strftime('%Y-%m-%d')
    # date_to_apply = datetime.strptime(date_into_string, '%Y-%m-%d')
    # user_data['date_of_birth'] = date_to_apply
    return user_data


def registration_to_datetime(user_data: Dict[str, Any]) -> Optional[str]:
    '''
    This function formats 'registered' dictionary as datetime and creates another dictionary 'registration_date'.
    which contains dates of registration in a more human readable format.
    '''
    dates_of_registration = user_data.get('registered')
    only_date = dates_of_registration.get('date')
    formatted_date = datetime.strptime(only_date, '%Y-%m-%dT%H:%M:%S.%fZ').date()
    user_data['registration_date'] = formatted_date.strftime('%B %d, %Y')
    return user_data

def calculate_user_age(user_data: Dict[str, Any]) -> Optional[str]:
    '''
    This function takes 'date' key from 'dob' dictionary and dynamically calculates the age of the user,
    then creates 'age' dictionary separately.
    '''

    today = datetime.today().year
    date_of_birth = user_data.get('date_of_birth')
    # date_of_birth_string = date_of_birth.strftime('%Y-%m-%d')
    date_year = datetime.strptime(date_of_birth, '%Y-%m-%d')
    year_of_birth = date_year.year
    age_of_user = today - year_of_birth
    user_data['age'] = age_of_user
    return user_data



def calculate_registration_age(user_data: Dict[str, Any]) -> Optional[str]:
    '''
    This function takes 'age' key from 'registered' dictionary and dynamically calculates the registration age of the user,
    then creates 'age_as_user' dictionary separately.
    '''
    today = datetime.today().year
    date_of_registration = user_data.get('registration_date')
    date_year = datetime.strptime(date_of_registration, '%B %d, %Y')
    year_of_registration = date_year.year
    age_as_user = today - year_of_registration
    user_data['age_as_user'] = age_as_user
    return user_data


def drop_unnecessary_keys(user_data: Dict[str, Any], keys_to_drop) -> Optional[str]:
    '''
    This function deletes columns that are not needed.
    '''
    for key in keys_to_drop:
        user_data.pop(key)
    return user_data



def reorder_keys(user_data: Dict[str, Any], keys_to_reorder) -> Optional[str]:
    '''
    This function reorders columns in a more logical way.
    '''
    reordered_data = {key: user_data[key] for key in keys_to_reorder if key in user_data}
    reordered_data.update({key: user_data[key] for key in user_data if key not in keys_to_reorder})
    user_data.clear()
    user_data.update(reordered_data)
    return user_data













