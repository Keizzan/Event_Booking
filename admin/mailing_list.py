# imports
from admin import database_connection as DB
from admin import encod 

#sql statements
get_salt = '''
SELECT salt FROM mailing_list WHERE id = 1
'''

get_email = '''
SELECT email FROM mailing_list WHERE id != 1
'''

add_email = '''
INSERT INTO mailing_list (email) VALUES ('%s')
'''

# pull all email list
def pull_mail():

    emails = []

    #create instance of db class
    db = DB.Event_database()
    
    #get salt 
    db.execute_function(get_salt)
    salt = encod.reversing_salt(db.cur.fetchone()[0])

    #execute sql statement
    db.execute_function(get_email)
    data = db.cur.fetchall()
    for i in data:
        emails.append(encod.decrypt_data(salt, i[0]))
    return emails

# add email to mailing list table
def add_mail(input):

    #create instance of db class
    db = DB.Event_database()

    #get full email list
    email_list = pull_mail()

    #check if email is already on list
    if input not in email_list:

        #get salt 
        db.execute_function(get_salt)
        salt = encod.reversing_salt(db.cur.fetchone()[0])

        #encrypt email
        email = encod.encrypt_data(salt, input)

        #insert data to table
        db.execute_function(add_email %(email))
