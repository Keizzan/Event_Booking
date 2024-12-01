# imports
from admin import database_connection as DB
from admin import encod

# create mailing list table
install_db_mailinglist= '''
    DROP TABLE IF EXISTS mailing_list;

    CREATE TABLE mailing_list(
    id serial PRIMARY KEY,
    email VARCHAR(250),
    salt VARCHAR(250)
    )
'''

#store salt
create_salt = '''
INSERT INTO mailing_list (salt) VALUES ('%s')
'''

# create admin table
install_db_admin = '''
    DROP TABLE IF EXISTS admin;

    CREATE TABLE admin(
    id serial PRIMARY KEY,
    login VARCHAR(250),
    password VARCHAR(250),
    salt VARCHAR(500)
    )'''

# populate admin table
create_admin_account = '''
    INSERT INTO admin (login, password, salt)
    VALUES ('ADMIN-USERNAME', '%s', '%s')'''

# create tables
def create_database():

    #create salt
    hidden_salt_admin = encod.creating_salt()
    hidden_salt_mailing_list = encod.creating_salt()

    salt = encod.reversing_salt(hidden_salt_admin)
    # encrypt password
    password = encod.encrypt_data(salt, 'password')## change password

    #create instance of database class
    db = DB.Event_database()
    
    # execute sql statements
    db.execute_function(install_db_mailinglist)
    db.execute_function(create_salt %(hidden_salt_mailing_list))
    db.execute_function(install_db_admin)     
    db.execute_function(create_admin_account %(password, hidden_salt_admin))


create_database()
print('Success')