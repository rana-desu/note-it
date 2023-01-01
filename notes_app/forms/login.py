from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email

class LogInForm(FlaskForm):
    email = StringField(
        "Email", 
        validators = [
            Email(
                message = "Login failed. Please use your email instead of username."
            ),
        ]
    )

    password = PasswordField("Password")
    submit = SubmitField("LOGIN")
    