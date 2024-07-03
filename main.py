from constants import URL, create_table_query # unused
from extract import extract_one_user, extract_all_users # unused
from transform import *
from load import * # import only things you require
import pandas as pd


# GENERAL COMMENCTS ABOUT THE PROGRAM
"""
1. __pycache__, .idea, should not be uploaded to github, they should be included in gitignore, so when you push to github, they are ignored

2. why is gitignore located in .idea ???????????????? it should be located in the root of the project

5, your function names are not descriptive enough, what does age_dob mean? what is age_user? try to come up with names
that summerize the functionality, for age_dob I would go with ** calculate_user_age **, for age_user I would go with 
** calculate_registration_date. ** drop_some_cols is a SIN AND NIGTHMARE what is anyone going to understand in there?

6. at this point you should be abel to write the same programm with OOP, next time try to follow OOP paradigm,
in this cases we could have had classes like: ExtractUser, TransformUser, LoadUser, DatabaseConnector, clearer and much organized.

++++++++++++++++++++++++++++ FUTURE CONSIDERATIONS ++++++++++++++++++++++++++++
7. when working on a project, good to have requirements.txt file, please look it up. when you use any kind of third party library
I have to install it when cloning your directory. better to have all of them in requirements. basically when you begin create .venv
and when you are done freeze the requirements. one of the ways is to execute following command:
    pip freeze > requirements.txt

8. we should start working more with git, when you are making some initial development, create a branch, work there, and then
create a pull request for me to review and approve. try watching videos from syllabus or read material about branching strategies.
"""



# Extraction part
extracted_users = extract_all_users(URL)

df = pd.DataFrame(extracted_users)

# Transformation part

# ABOUT TRANSFORMATION PART
###################################################################################################
# this may work but might lead to some erros if any mistakes are made (easily could happen)       #
# in addition to that, you are overrwiting over the same df too many times, which is not efficient# 
# if OOP was used you would have been able to chain this functions all together and would be      #
# more beautiful and readable, but for now if we want to stick with this, please take a look      #
# at !!!!pipe!!!!  functionality that pandas offers and try to use it, here is the link for it    #
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pipe.html                         #
###################################################################################################

# you can add logging statements here, to see how the progress is going

df = full_name(df) # bad function naming
df['location'] = df.apply(get_location, axis=1)
df['initials'] = df['name'].apply(initials) # initials ---> bad function naming
df = parsing_phoneloc(df)
df = validate_emails(df)
df = dob_to_datetime(df)
df = reg_to_datetime(df)
df = age_dob(df) # bad function naming
df = age_user(df) # bad function naming
df = drop_some_cols(df) # bad function naming
df = reorder_cols(df)

# Loading part
load_to_raw_data(extracted_users)

# this part is tricky, read carefully
############################################################################################
# first, you are creating a connection to a db and using it for create_table func          # 
# that makes sense, then you need to load into the table, so in the func, you are          # 
# creating another connection and then closing it. keep in mind that opening and closing   #
# connections is a heavy operation, so why dont you create one conn outside those funcs and#
# use that connection for the functions as arguments?                                      #
############################################################################################

################################### EXAMPLE #####################################
# create conn here conn = whatever code goes here                               #
# call create table function with that conn                                     #
# call load_data_to_database and pass conn as one of the arguments              #
# close the connections at last                                                 #
#################################################################################

# SEPARATE COMMENT
# you have dbname, user, password, host, port defined in settings.py why are you not using them??
# do not hardcode things like that
conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", port='5432')
create_table(conn) # what table? better to pass the query as an argument, more readable

# dbname, user, host, password, port where are they imported from?
# as I understand, you are importing them in load.py and then importing load.py to main using *. that is horrible, import the constants
# directly in the main.py, you do not need them in the load.py
load_data_to_database(df, dbname, user, host, password, port)
