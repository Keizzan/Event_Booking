from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, EmailField, TelField
from wtforms.validators import InputRequired, Email, NumberRange, ValidationError
import phonenumbers



# custom phone number validation
def phone_number_validator(form, field):
    try:
        phone_number = phonenumbers.parse(field.data, "GB")
        if not (phonenumbers.is_valid_number(phone_number)):
            raise ValidationError('Invalid Phone Number')
    except:
        raise ValidationError('Invalid Phone Number')

# validation class for user booking form 
class User(FlaskForm):
    fname = StringField("Name", validators=[InputRequired()])
    lname = StringField("Surname", validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email(check_deliverability=True)])
    phone = TelField('Phone', validators=[InputRequired(), phone_number_validator])
    booking = IntegerField('Number of bookings', validators=[InputRequired(), NumberRange(min=1, max=10)])
    mailing_list = BooleanField('Mailing list', default='checked')
    terms_and_condition = BooleanField('Terms & Conditions', validators=[InputRequired()])

# validation class for admin login
class Login(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


