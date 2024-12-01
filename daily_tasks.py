from admin import (
    pull_tables,
    pull_event,
    pull_booking,
    encod,
    update_event,
    email_classes,
    email_templates,
)
from admin import DB_config as DB
import datetime, schedule, time, subprocess, gzip, datetime, os

def confirm_event():
    # get all events
    tables = pull_tables.show_tables()

    # loop through upcoming events and find
    # event which is scheduled next day
    for i in tables:
        
        # change str from table name in datetime object
        date = datetime.date(int(i[-8:-4]), int(i[-10:-8]), int(i[-12:-10]))
        today = datetime.date.today()

        # check if difference is 1 day
        if date - today == datetime.timedelta(1):
            
            # pull event details
            event = pull_event.pull_event(i)[0]
            status = event[-1]

            # check if status is upcoming
            if status == "upcoming":

                # pull booking details
                booking_details, salt = pull_booking.pull_records(i)

                # create dict for records
                records_dict = {}
                for detail in booking_details:
                    for a in detail:
                        records_dict.update(
                            {
                                a[0]: {
                                    "fname": encod.decrypt_data(salt, a[1]),
                                    "email": encod.decrypt_data(salt, a[3]),
                                }
                            }
                        )

                # send emails
                # reminder to customers
                for record in records_dict.values():
                    email_classes.Remider(
                        record["email"],
                        email_templates.reminder_txt,
                        email_templates.remider_html,
                        event[1],
                        date.strftime("%d/%m/%Y"),
                        event[3][:2] + ":" + event[3][2:],
                    ).send()

                # reminder to admin
                email_classes.Admin_reminder(
                    email_templates.admin_reminder,
                    event[1],
                    date.strftime("%d/%m/%Y"),
                    event[3][:2] + ":" + event[3][2:],
                ).send()

                # change status to confirmed
                update_event.update_event_status(i,'confirmed')


#backup db to file in admin/backups folder 
# db_name_backup_date today.gz
def db_backup(database_name, user=DB.user, password=DB.password, host=DB.host, port=DB.port):

    #create backups dir
    os.makedirs('admin/backups', exist_ok=True)

    #pgdump for terminal with db credentials
    cmd = ['pg_dump', f'postgresql://{user}:{password}@{host}:{port}/{database_name}']

    #create a backup file and write line by line
    with gzip.open(f'admin/backups/{database_name}_backup_{datetime.datetime.now().strftime('%d%m%Y')}.gz', 'wb') as f:
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)

        for stdout_line in iter(popen.stdout.readline, ""):
            f.write(stdout_line.encode('utf-8'))

        popen.stdout.close()
        popen.wait()


#delete old backups
def delete_old_backups():
    
    #read files in dir
    files = os.listdir('admin/backups/')
    #set today date
    today = datetime.date.today()

    #go through files and compare dates if older than 3 days delete file
    for file in files:
        backup_date = datetime.date(int(file[-7:-3]), int(file[-9:-7]), int(file[-11:-9]))
        if today - backup_date >= datetime.timedelta(3):
            os.remove(f'admin/backups/{file}')


#first scheduler
#each day at 3pm
confirm = schedule.Scheduler()
confirm.every().day.at('15:00').do(confirm_event)

#second scheduler 
#each day at 23:50 & 23:55
backups = schedule.Scheduler()
backups.every().day.at('23:50').do(db_backup, database_name='')# active db
backups.every().day.at('23:55').do(db_backup, database_name='')# past events db

#third scheduler
#each day at 00:05
cleanup = schedule.Scheduler()
cleanup.every().day.at('00:05').do(delete_old_backups)

while True:
    confirm.run_pending()
    backups.run_pending()
    cleanup.run_pending()
    time.sleep(1)

