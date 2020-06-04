from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField


class SearchForm(FlaskForm):
    query = StringField('Запрос', description="Например, “мелирование”")  # validators=[InputRequired(), Length(min=2, max=50)]
    submit = SubmitField('Поиск')
