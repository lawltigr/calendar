from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Length(min=6)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm your password", validators=[DataRequired(), EqualTo("password", message="Passwords do not match")])
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("This username is already taken")
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("This email already has an account")
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
class CourseForm(FlaskForm):
    title = StringField("Course title", validators=[DataRequired(), Length(max=150)])
    description=TextAreaField("Description", validators=[Length(max=2000)])
