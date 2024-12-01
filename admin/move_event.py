# imports
from admin import database_connection as DB
from admin import DB_config
import pandas as pd
from sqlalchemy import create_engine

#sql statement pull table
pull_table = '''
SELECT * FROM %s ORDER BY id
'''

# create new table in legacy database
create_legacy_table = """
CREATE TABLE %s (
id INT(12) PRIMARY KEY,
event_name VARCHAR(250),
event_date VARCHAR(8),
event_time VARCHAR(4),
event_price VARCHAR(4),
event_limit VARCHAR(3),
event_desc TEXT,
user_fname VARCHAR(250),
user_lname VARCHAR(250),
user_email VARCHAR(250),
user_phone VARCHAR(250),
user_booking VARCHAR(2),
status VARCHAR(10)
)
"""


# create connection with sqlalchemy to postgres 
# allow to export data from dataframe to postgres with pandas
con_string = 'postgresql+psycopg://%s:%s@%s/%s' % (DB_config.user, DB_config.password, DB_config.host, DB_config.past_name)
engine_db = create_engine(con_string)

#past event database connection with engine from sqlalchemy
conn = engine_db.connect()

# function to transfer table to legacy database
def event(table_name, status):
    
    #create instance of database class
    db = DB.Event_database()

    # create dataframe from source table 
    # & change status to cancelled
    table_data = pd.read_sql(pull_table %(table_name), db.conn)

    #change status of event
    table_data.at[0,'status']= status

    #drop table in event database
    db.execute_function('DROP TABLE %s' %(table_name))

    # write new table on legacy database
    table_data.to_sql(table_name, conn)


