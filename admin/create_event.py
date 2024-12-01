# imports
from admin import database_connection as DB
from admin import encod

# sql statement to create new table
create_table = """
CREATE TABLE %s (
id serial PRIMARY KEY,
event_name VARCHAR(250),
event_date VARCHAR(10),
event_time VARCHAR(10),
event_price VARCHAR(10),
event_limit VARCHAR(10),
event_desc TEXT,
status VARCHAR(10),
salt VARCHAR(500),
user_fname VARCHAR(500),
user_lname VARCHAR(500),
user_email VARCHAR(500),
user_phone VARCHAR(500),
user_booking VARCHAR(100)
)
"""

# statement to fill first record in db (header)
fill_event = """
INSERT INTO %s (event_name, event_date, event_time, event_price,
event_limit, event_desc, salt, status) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s' , 'upcoming')
"""

# create new event
def create_event(name, date, time, price, limit, desc):
    
    name = name.replace(' ','_')

    #set name of table
    table_name = name+date+time

    #create salt
    salt = encod.creating_salt()

    #create instance of database class
    db = DB.Event_database()
    
    #execute sql statements
    db.execute_function(create_table %(table_name))
    db.execute_function(fill_event % (table_name, name, date, time, price, limit, desc, salt))

