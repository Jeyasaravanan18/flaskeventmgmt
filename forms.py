# eventhive/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, TextAreaField, RadioField
from wtforms.fields import DateTimeLocalField  # ✅ Modern DateTimeLocalField for browser compatibility
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models.models import User

# --------------------------- Registration Form --------------------------- #
class RegistrationForm(FlaskForm):
    """
    Form for users to create a new account.
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    # Role dropdown
    role = SelectField('Register as',
                       choices=[('Student', 'Student'), ('Organizer', 'Organizer')],
                       validators=[DataRequired()])
    
    submit = SubmitField('Sign Up')

    # Validate unique username
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    # Validate unique email
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose a different one.')

# --------------------------- Login Form --------------------------- #
class LoginForm(FlaskForm):
    """
    Form for users to login.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

# --------------------------- Event Form --------------------------- #
class EventForm(FlaskForm):
    """
    Form for users to create a new event.
    """
    title = StringField('Event Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    
    # ✅ Updated field: DateTimeLocalField for modern HTML5 datetime input
    event_date = DateTimeLocalField('Event Date and Time',
                                    format='%Y-%m-%dT%H:%M',
                                    validators=[DataRequired()])
    
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Create Event')

# --------------------------- Feedback Form --------------------------- #
class FeedbackForm(FlaskForm):
    """
    Form for students to submit event feedback.
    """
    rating = RadioField('Rating', 
                        choices=[('5', 'Excellent'), 
                                 ('4', 'Good'), 
                                 ('3', 'Average'), 
                                 ('2', 'Poor'), 
                                 ('1', 'Terrible')],
                        validators=[DataRequired()])
    comment = TextAreaField('Comment (Optional)', render_kw={'rows': 5})
    submit = SubmitField('Submit Feedback')
