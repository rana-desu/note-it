from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length


class NoteForm(FlaskForm):
    
    title = StringField(
        "Title",
        validators = [
            InputRequired(),
            Length(
                min = 3,
                max = 60,
                message = "The title should be between 3 to 60 characters."
            )
        ]
    )

    description = StringField("Description")
    submit = SubmitField("SUBMIT")
