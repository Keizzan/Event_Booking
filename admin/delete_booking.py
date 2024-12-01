# imports
from admin import database_connection as DB

#sql statement to delete record record
delete = '''
DELETE FROM %s WHERE id = %s
'''

#delete booking function
def delete_booking(table_name, id):

    ##create instance of database class
    db = DB.Event_database()
            
    #execute sql statement
    db.execute_function(delete %(table_name, id))
