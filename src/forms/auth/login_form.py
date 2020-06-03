from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length


class LogInForm(FlaskForm):
    email = StringField('Логин', validators=[InputRequired(), Email(), Length(max=50)])
    password = PasswordField('Пароль', validators=[InputRequired(), Length(max=100)])
    log_in = SubmitField('Войти')
