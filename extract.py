import sys

from constants import URL, HEADERS
from typing import List
from dataclasses import dataclass
from datetime import datetime
import logging
import requests
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class UserData:
    gender: str
    location: dict
    email: str
    registered: dict
    nat: str

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
    street: Street
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

class RandomUserAPI:
    def __init__(self) -> None:
        self.url = URL
        self.headers = HEADERS

    def extract_all_data(self) -> List[UserData]:
        all_data = []
        next_page_url = self.url

        while next_page_url:
            logger.info(f"Fetching data from {next_page_url}")

            try:
                response = requests.get(next_page_url, headers=self.headers)
                response.raise_for_status()

                data = response.json()
                users = data.get('results', [])
                all_data.extend(users)
                logger.info(f"Fetched {len(users)} users")
                for user in users:
                    all_data.append(UserData(**user))
            except Exception as e:
                logger.error(f"Error fetching or parsing data: {e}")
            finally:
                 next_page_url = data.get('next_page_url', None)
            if len(all_data) >= 10:
                for user in all_data[:10]:
                    logger.info(f"Extracted user: {user}")
            else:
                logger.warning(f"Extracted only {len(all_data)} users. Might be less than expected.")
        return all_data

    def save_to_json(self, data: List[UserData], filename: str) -> None:
        with open(filename, "w") as file:
            json.dump([vars(user) for user in data], file, indent=4)


