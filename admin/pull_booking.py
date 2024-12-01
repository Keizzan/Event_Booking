# imports
from admin import database_connection as DB
from admin import encod

# sql statement
get_salt = """
SELECT (salt) FROM %s WHERE id = 1
"""

pull_booking = """
SELECT (id, user_fname, user_lname, user_email, user_phone, user_booking) FROM %s WHERE id != 1 ORDER BY id
"""

pull_emails = """
SELECT (user_email) FROM %s WHERE id !=1 ORDER BY id
"""

pull_total_booking = """
SELECT (user_booking) FROM %s WHERE id != 1"""


# fetch data from specific event table
def pull_records(table_name):

    # create instance of database class
    db = DB.Event_database()

    # execute sql statement to pull salt
    db.execute_function(get_salt % (table_name))

    # clean salt
    salt = encod.reversing_salt(db.cur.fetchone()[0])

    # execute sql statement
    db.execute_function(pull_booking % (table_name))

    # store data in records variable
    records = db.cur.fetchall()

    # return records in list
    return records, salt


# fetch data from specific event table
def pull_records_past(table_name):

    # create instance of database class
    db = DB.PastEvent_database()

    # execute sql statement to pull salt
    db.execute_function(get_salt % (table_name))

    # clean salt
    salt = encod.reversing_salt(db.cur.fetchone()[0])

    # execute sql statement
    db.execute_function(pull_booking % (table_name))

    # store data in records variable
    records = db.cur.fetchall()

    # return records in list
    return records, salt


# fetch user bookings
def pull_user_booking(table_name):

    # create instance of database class
    db = DB.Event_database()

    # execute sql statement
    db.execute_function(pull_total_booking % (table_name))

    # store data in records variable
    records = db.cur.fetchall()

    return records


def get_emails(table_name):

    db = DB.Event_database()

    db.execute_function(get_salt % (table_name))

    salt = encod.reversing_salt(db.cur.fetchone()[0])

    # execute sql statement
    db.execute_function(pull_emails % (table_name))

    # store data in records variable
    records = db.cur.fetchall()

    return records, salt
