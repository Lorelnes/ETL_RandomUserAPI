URL = "https://randomuser.me/api"

HEADERS = {"Accept": "applicatoon/json"}

create_table_query = """
CREATE TABLE IF NOT EXISTS RandomUsersAPI (
                   id SERIAL PRIMARY KEY,
                   gender VARCHAR(255),
                   name VARCHAR(255),
                   location TEXT,
                   email VARCHAR(255),
                   login VARCHAR(255),
                   dob DATE,
                   registered DATE,
                   nat VARCHAR(255),
        
);
"""

insert_data_query = """
INSERT INTO RandomUsersAPI (gender, name, location, email, login, dob, registered, nat)
VALUES %s
"""