import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email_template:
    def __init__(self, subject, receiver):
        
        self.smtp_server = "" # MAILING SERVER
        self.sender = "" #EMAIL ADDRESS
        self.password = "" # PASSWORD
        self.port = 000 # PORT
        self.receiver = receiver
        self.subject = subject
        self.context = ssl.create_default_context()

        self.message = MIMEMultipart("alternative")
        self.message["From"] = self.sender
        self.message["Subject"] = self.subject
        self.message["To"] = self.receiver

    def send(self):
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=self.context) as server:
                server.login(self.sender, self.password)
                server.sendmail(self.sender, self.receiver, self.message.as_string())
        except Exception as e:
            print(f'Failed to send email: {e}')

class Confimation(Email_template):
    def __init__(self, receiver, text_version, html_version, name):
        super().__init__('Booking Confirmed', receiver)

        # Turn these into plain/html MIMEText objects
        txt = MIMEText(text_version.format(name=name), "plain")
        htxt = MIMEText(html_version.format(name=name), "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        self.message.attach(txt)
        self.message.attach(htxt)

class Admin_confirmation(Email_template):
    def __init__(self, text_version, fname, lname, booking, event):
        super().__init__('Booking confirmed', 'ADMIN@MAIL.COM')# SET 2 ARGUMENT

        txt = MIMEText(text_version.format(fname=fname, lname=lname, booking=booking,event=event), 'plain')

        self.message.attach(txt)

class Cancellation(Email_template):
    def __init__(self, receiver, text_version, html_version, event, date, time):
        super().__init__('Event Cancelled', receiver)

        txt = MIMEText(text_version.format(event=event, date=date, time=time), "plain")
        htxt = MIMEText(html_version.format(event=event, date=date, time=time), "html")

        self.message.attach(txt)
        self.message.attach(htxt)

class Remider(Email_template):
    def __init__(self, receiver, text_version, html_version, event, date, time):
        super().__init__('Upcoming Event', receiver)

        # Turn these into plain/html MIMEText objects
        txt = MIMEText(text_version.format(event=event, date=date, time=time), "plain")
        htxt = MIMEText(html_version.format(event=event, date=date, time=time), "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        self.message.attach(txt)
        self.message.attach(htxt)

class Admin_reminder(Email_template):
    def __init__(self, text_version, event, date, time):
        super().__init__('Upcoming Event', 'ADMIN@MAIL.COM')# SET 2 ARGUMENT

        txt = MIMEText(text_version.format(event=event, date=date, time=time), "plain")
        self.message.attach(txt)
