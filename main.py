from constants import URL
from extract import extract_one_user
from dataclasses import dataclass
import pandas as pd
import requests
import logging

# Extraction part

# Calling function for extracting one user
one_user = extract_one_user(URL)

# def extract_all_users(URL: str) -> dict:
#     """
#     Extracts 1000 user data from the URL and returns dictionary:
#
#     Args:
#          URL(type hint: str) : the URL from which we extract the data.
#
#     Returns:
#          dict: A dictionary containing the extracted data.
#
#     Logs:
#          INFO: logs the number of extracted users.
#          WARNING: logs a message if we already extracted 1000 users.
#     """
#     extracted_users = {}
#     for i in range(10):
#         user = extract_one_user(URL)
#         if user:
#             extracted_users[i] = user
#             if extracted_users:
#                 logging.info(f"Extracted {len(extracted_users)} users")
#             else:
#                 logging.warning("No users extracted")
#
#     return extracted_users

df = pd.DataFrame.from_dict(one_user)
# extracted_users = extract_all_users(URL)


# Transformation part

# Defining column names and turning data into dataframe
# df = pd.DataFrame.from_dict(extracted_users)


df['Name'] = df['name'].apply(lambda x: f"{x.get('first', '')} {x.get('last', '')}")
df.to_json("example.json", orient="index", indent=4)
print(df)