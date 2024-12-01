# imports
from admin import database_connection as DB

# sql statement
event_details= '''
SELECT (id, event_name, event_date, event_time, event_price, event_limit, event_desc, status) FROM %s where id = 1
'''

# pull first record (header) of table
def pull_event(table_name):
    
    #create instance of database class
    db = DB.Event_database()
            
    #execute sql statement
    db.execute_function(event_details %(table_name))

    # store data in records variable
    records = db.cur.fetchone()

    return records

def pull_pastevent(table_name):
    
    #create instance of database class
    db = DB.PastEvent_database()
            
    #execute sql statement
    db.execute_function(event_details %(table_name))

    # store data in records variable
    records = db.cur.fetchone()

    return records