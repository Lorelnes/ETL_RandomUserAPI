from constants import URL
from typing import Dict
import requests
import logging

logging.basicConfig(level=logging.INFO)

def extract_all_data(URL: str) -> dict:
    try:
        response = requests.get(url=URL)
        response.raise_for_status()
        data = response.json()
        logging.info("Data retrieved successfully")

        user_data = data.get('results', {})
        if user_data:
            logging.info("Extracted user data")
            return user_data[0]
        else:
            logging.warning("No user data found")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from {URL}: {e}")

data = extract_all_data(URL)
print(data)

