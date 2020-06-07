from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, Length


class LogInForm(FlaskForm):
    email = EmailField('Логин', validators=[InputRequired(), Email(), Length(min=5, max=50)])
    password = PasswordField('Пароль', validators=[InputRequired(), Length(min=5, max=50)])
    log_in = SubmitField('Войти')
