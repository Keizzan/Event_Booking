# Event_Booking

Python program with PostgreSQL database and Stripe payment system

Eeach event is seperate table in db with first record of event information like date, time and name, following with records of signed up customers.

requirements.txt holds all required libs 

set in admin/DB_config.py variables to connect to database
set in app.py stripe keys to connect to your stripe account

in admin/email_classes.py - set email confings
in admin/email_templates.py - set your email templates

daily_tasks.py contains scheduled functions to run backup of your databases & check your upcoming events - run this seperately
