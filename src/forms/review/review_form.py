from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Length, NumberRange


class ReviewForm(FlaskForm):
    content = TextAreaField('Текст отзыва', validators=[InputRequired(), Length(min=10, max=1000)])
    rating = IntegerField('Оценка', validators=[InputRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Оставить отзыв')
