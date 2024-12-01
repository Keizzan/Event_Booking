#imports
from admin import database_connection as DB
from admin import encod

#sql to get login details
sql = 'SELECT * FROM admin WHERE id = 1'


def login(login, password):

    #create instance of database class
    db = DB.Event_database()

    #execute sql statement
    db.execute_function(sql)
    rec = db.cur.fetchone()

    #store data in variable data 
    data = {'id':rec[0], 'login':rec[1], 'password':rec[2], 'salt':rec[3]}

    #clean salt
    clean_salt = encod.reversing_salt(data['salt'])

    #decrypt password from db
    org_password = encod.decrypt_data(clean_salt, data['password'])
    org_login = data['login']

    # check if input is matching db
    if login == org_login and password == org_password:
        return True
    else:
        return False
    
