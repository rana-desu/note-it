from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Length, Email, EqualTo
import re


def validate_username(form, field):
    """
    Validating username on the basis of whitelisted words
    """
    username = field.data
    USERNAME_REGEX = re.compile("^[a-zA-Z0-9_]+$")

    if USERNAME_REGEX.match(username) is None:
        raise ValidationError("Usernames can only use letters, numbers, and underscores.")


class SignUpForm(FlaskForm):
    username = StringField(
        "Username", 
        validators = [
            InputRequired(
                message = "The username field is required."
            ), 
            Length(
                min = 3, 
                max = 30, 
                message = "The username must be between 3 to 30 characters."
            ), 
            validate_username,
        ]
    )

    email = StringField(
        "Email", 
        validators = [
            InputRequired(
                message = "The email field is required."
            ), 
            Email(
                message = "Invalid Email Address."
            ),
        ]
    )

    password = PasswordField(
        "Password",
        validators = [
            InputRequired(
                message = "The password field is required."
            ), 
            Length(
                min = 10,
                max = 30,
                message = "The password must be between 10 to 30 characters."
            ),
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password", 
        validators = [
            InputRequired(
                message = "The confirm password field is required."
            ),
            EqualTo(
                "password", 
                message = "Both the passwords must match."
            ),
        ]
    )

    submit = SubmitField("SIGNUP")
    