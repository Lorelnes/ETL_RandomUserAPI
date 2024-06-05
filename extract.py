from constants import URL, HEADERS, PARAMS
from typing import List
from dataclasses import dataclass
import logging
import requests
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class UserData:
    gender: str
    name: dict
    location: dict
    email: str
    login: dict
    dob: str
    registered: dict
    phone: str
    cell: str
    id: dict
    picture: dict
    nat: str

class RandomUserAPI:
    def __init__(self) -> None:
        self.url = URL

    def fetch_all_user_data(self) -> List[UserData]:
        results = []
        page = 1
        try:
            while True:
                params = PARAMS.copy()
                params["page"] = page
                response = requests.get(self.url, headers=HEADERS, params=params)
                response.raise_for_status()
                data = response.json()
                users = data.get("results", [])
                for user in users:
                    results.append(UserData(**user))
                if len(users) < PARAMS["results"]:
                    break
                page += 1
        except requests.RequestException as e:
            logger.error(f"Error fetching user data: {e}")
        return results

    def save_to_json(self, data: List[UserData], filename: str) -> None:
        with open(filename, "w") as file:
            json.dump([vars(user) for user in data], file, indent=4)

if __name__ == "__main__":
    random_user_api = RandomUserAPI()
    all_user_data = random_user_api.fetch_all_user_data()
    logger.info(f"Total users fetched: {len(all_user_data)}")
    random_user_api.save_to_json(all_user_data, "user_data.json")
    logger.info("User data saved to user_data.json")