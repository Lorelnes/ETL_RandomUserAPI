from constants import URL
from typing import Dict, List
import requests
import logging

logging.basicConfig(level=logging.INFO)

def extract_one_user(URL: str) -> List[Dict]:
    """
    Fetches data from URL, parses JSON response, and extracts
    the first user data element from 'results' key.

    Args:
    URL(str): URL to get data from.

    Returns:
    dict: The first user data element if found, otherwise None.
    """

    try:
        response = requests.get(url=URL)
        response.raise_for_status()
        data = response.json()
        logging.info("Data retrieved successfully")

        user_data = data.get('results', [])
        if user_data:
            logging.info("Extracted user data")
            return user_data[0]
        else:
            logging.warning("No user data found")
            return []

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from {URL}: {e}")

def extract_all_users(URL: str) -> List[dict]:
    """
    Extracts 1000 user data from the URL and returns dictionary:

    Args:
         URL(type hint: str) : the URL from which we extract the data.

    Returns:
         dict: A dictionary containing the extracted data.
    """

    extracted_users = [] # try not to save users in list and work on each response as you retrieve it, we will do batch processing later
    for i in range(10000): # why hardcoding 5 as the number of users? this should be in the main.py
        user = extract_one_user(URL)
        if user:
            extracted_users.append(user)
            if extracted_users:
                logging.info(f"Extracted {len(extracted_users)} users")
            else:
                logging.warning("No users extracted")

    return extracted_users



