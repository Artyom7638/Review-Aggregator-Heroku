from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import InputRequired, Length


class NameSurnameForm(FlaskForm):
    name = StringField('Имя', validators=[InputRequired(), Length(min=2, max=25)])
    surname = StringField('Фамилия', validators=[InputRequired(), Length(min=2, max=25)])
