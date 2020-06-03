from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import InputRequired, Length


class SearchForm(FlaskForm):
    query = StringField('Запрос', description="Например, “мелирование”")  # validators=[InputRequired(), Length(min=2, max=50)]
    # search = SubmitField('Поиск')
