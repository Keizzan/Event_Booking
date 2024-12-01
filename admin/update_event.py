# imports
from admin import database_connection as DB

#sql statement update event
update = '''
UPDATE %s SET 
event_name = '%s', 
event_date = '%s',
event_time = '%s',
event_price = '%s',
event_limit = '%s',
event_desc = '%s'
WHERE id = 1
'''

update_status = '''
UPDATE %s SET 
status = '%s'
WHERE id = 1'''

#update function
def update_event(table_name, name, date, time, price, limit, desc):

    #create instance of database class
    db = DB.Event_database()

    # execute sql statement to create table
    db.execute_function(update % (table_name, name, date, time, price, limit, desc))

def update_event_status(table_name, status):

    db = DB.Event_database()

    db.execute_function(update_status %(table_name, status))
