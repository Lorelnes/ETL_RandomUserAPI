from psycopg2 import sql


URL = "https://randomuser.me/api"

keys_to_drop = ['login', 'cell', 'picture', 'dob', 'registered', 'id']

keys_to_reorder = ['gender', 'name', 'initials', 'location', 'date_of_birth', 'age', 'registration_date', 'age_as_user',
                      'email', 'phone', 'nat']

table_schema = {
    "id": "SERIAL PRIMARY KEY",
    "gender": "VARCHAR(255)",
    "name": "VARCHAR(255)",
    "initials": "VARCHAR(255)",
    "location": "VARCHAR(MAX)",
    "date_of_birth": "TEXT",
    "age": "INTEGER",
    "registration_date": "DATE",
    "age_as_user": "INTEGER",
    "email": "VARCHAR(255)",
    "phone": "VARCHAR(255)",
    "nat": "VARCHAR(255)"
}

create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS RandomUserAPI ()").format(table_schema)


insert_data_query = """
INSERT INTO RandomUsersAPI (gender, name, initials, location, date_of_birth, age, registration_date, age_as_user, email, phone, nat)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

