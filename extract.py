from constants import URL, HEADERS
from typing import List
from dataclasses import dataclass
from datetime import datetime
import logging
import requests
import json

logging.basicConfig(level=logging.INFO)

@dataclass
class Name:
    title: str
    first: str
    last: str

@dataclass
class Street:
    number: int
    name: str

@dataclass
class Location:
    street: 'Street'
    state: str
    country: str


@dataclass
class Login:
    username: str
    password: str

@dataclass
class Dob:
    date: datetime
    age: int

@dataclass
class Registered:
    date: datetime
    age: int

@dataclass
class UserData:
    """
        Represents a user object obtained from the Random User API.

        Attributes:
            gender (str): The user's gender.
            location (dict): A dictionary containing user's location details.
            email (str): The user's email address.
            nat (str): The user's nationality.
        """
    gender: str
    name: Name
    location: Location
    email: str
    login: Login
    dob: Dob
    registered: Registered
    nat: str

class RandomUserAPI:
    def __init__(self) -> None:
        """
               Initializes a RandomUserAPI object with the provided URL and headers.

               Args:
                   None
        """
        self.url = URL
        self.headers = HEADERS

    def extract_all_data(self) -> List[UserData]:
        """
                Extracts all user data from the Random User API, respecting pagination.

                Returns:
                    List[UserData]: A list of UserData objects containing user information.
                """
        all_data = []
        next_page_url = self.url

        while next_page_url:
            logging.info(f"Fetching data from {next_page_url}")
            try:
                response = requests.get(next_page_url, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                users = data.get('results', [])
                all_data.extend(users)
                logging.info(f"Fetched {len(users)} users")
                for user in users:
                    user_data = {
                        "gender": user.get('gender'),
                        "name": user.get('name'),
                        "location": user.get('location'),
                        "email": user.get('email'),
                        "login": user.get('login'),
                        "dob": user.get('dob'),
                        "registered": user.get('registered'),
                        "nat": user.get('nat'),
                    }
                    all_data.append(UserData(**user_data))
                    next_page_url = data.get('next_page_url', None)
            except requests.exceptions.RequestException as e:
                   logging.error(f"Error fetching or parsing data: {e}")
            finally:
                 next_page_url = data.get('next_page_url', None)
            # if len(all_data) >= 10:
            #     for user in all_data[:10]:
            #         logging.info(f"Extracted user: {user}")

            # else:
            #     logging.warning(f"Extracted only {len(all_data)} users. Might be less than expected.")
        return all_data

    def save_to_json(self, data: List[UserData], filename: str) -> None:
        """
                Saves a list of UserData objects to a JSON file.

                Args:
                    data (List[UserData]): The list of user data to save.
                    filename (str): The filename for the JSON file.
                """
        with open(filename, "w") as file:
            json.dump([vars(user) for user in data], file, indent=4)

RandomUserAPI().extract_all_data()
