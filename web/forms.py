from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class InputKeyForm(FlaskForm):
    input_key = StringField('InputKey', validators=[DataRequired()])
    submit = SubmitField('Search')