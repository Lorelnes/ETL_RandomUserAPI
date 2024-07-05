URL = "https://randomuser.me/api"

# this query is hardcoded, try to define schema beforhand and then dinamically join it 
# for example:

# table_schema = {
#     "id": "SERIAL PRIMARY KEY",
#     "gender": "VARCHAR(255)"
#     -----and so on-----
# }


create_table_query = """
CREATE TABLE IF NOT EXISTS RandomUsersAPI (
                   id SERIAL PRIMARY KEY,
                   gender VARCHAR(255),
                   name VARCHAR(255),
                   initials VARCHAR(255),
                   location TEXT,
                   date_of_birth DATE,
                   age INTEGER,
                   registration_date DATE,
                   age_as_user INTEGER,
                   email VARCHAR(255),
                   phone VARCHAR(255),
                   nat VARCHAR(255)
                   ); """

insert_data_query = f"""
INSERT INTO RandomUsersAPI (gender, name, initials, location, date_of_birth, age, registration_date, age_as_user, email, phone, nat)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


# you can have columns to reorder here
# columns_to_reorder = ['gender', 'name', 'initials', 'location', 'date_of_birth', 'age', 'registration_date', 'age_as_user',
#                  'email', 'phone', 'nat']