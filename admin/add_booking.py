# imports
from admin import database_connection as DB
from admin import encod 

get_salt = '''
SELECT salt FROM %s WHERE id = 1
'''

#sql statement to fill new record
fill_booking = """
INSERT INTO %s (user_fname, user_lname, user_email, user_phone, user_booking) VALUES ('%s', '%s', '%s', '%s', '%s')
"""



#add booking function
def add_booking(table_name, fname, lname, email, phone, booking):

    #create instance of database class
    db = DB.Event_database()
    
    #execute sql statement to pull salt
    db.execute_function(get_salt %(table_name)) 

    #clean salt      
    salt = encod.reversing_salt(db.cur.fetchone()[0])

    #encrypt data
    fname = encod.encrypt_data(salt, fname)
    lname = encod.encrypt_data(salt, lname)
    email = encod.encrypt_data(salt, email)
    phone = encod.encrypt_data(salt, phone)

    #insert data to table
    db.execute_function(fill_booking %(table_name, fname, lname, email, phone, booking))