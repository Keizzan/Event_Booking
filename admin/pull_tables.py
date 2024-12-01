# imports
from admin import database_connection as DB

# sql pull tables
show = '''
SELECT *
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND 
schemaname != 'information_schema';
'''

# function return list of tables without 
# mailing_list and admin tables
def show_tables():

    # empty list to populate list of tables
    table_list = []

    #create instance of database class
    db = DB.Event_database()

    # execution sql statement
    db.execute_function(show)

    # fetch data from db
    data = db.cur.fetchall()
            
    # populate list of tables 
    # without admin and mailing_list
    for i in data:
        if i[1] != 'admin' and i[1] != 'mailing_list':
            table_list.append(i[1])
            
    return table_list

def show_past_tables():

    # empty list to populate list of tables
    table_list = []

    #create instance of database class
    db = DB.PastEvent_database()

    # execution sql statement
    db.execute_function(show)

    # fetch data from db
    data = db.cur.fetchall()
            
    # populate list of tables 
    for i in data:
        table_list.append(i[1])
                
    return table_list


