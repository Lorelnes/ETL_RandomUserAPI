from constants import URL, create_table_query, table_schema, keys_to_drop, keys_to_reorder
from extract import extract_one_user
from transform import get_full_name, get_location, create_initials_column, parsing_phone_numbers, UserEmail, validate_emails, dateofbirth_to_datetime, registration_to_datetime, calculate_user_age, calculate_registration_age, drop_unnecessary_keys, reorder_keys
from load import load_to_raw_data, create_table, load_data_to_database
from settings import dbname, user, host, password, port
from psycopg2 import sql
import pandas as pd
import json
import psycopg2

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
create_table(conn, create_table_query)

for i in range(3):
    user_data = extract_one_user(URL)
    get_full_name(user_data)
    get_location(user_data)
    create_initials_column(user_data)
    parsing_phone_numbers(user_data)
    validate_emails(user_data)
    dateofbirth_to_datetime(user_data)
    registration_to_datetime(user_data)
    calculate_user_age(user_data)
    calculate_registration_age(user_data)
    drop_unnecessary_keys(user_data, keys_to_drop)
    reorder_keys(user_data, keys_to_reorder)

# Loading part

data = tuple(v for v in user_data.values())
load_data_to_database(data, conn)
conn.close()
