from wtforms import PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, Email

from src.forms.name_surname_form import NameSurnameForm
from src.forms.profile.client_profile_edit_form import ClientProfileEditForm
from src.models.client import Client


class ClientRegistrationForm(NameSurnameForm):
    email = EmailField('Почта', validators=[InputRequired(), Email(), Length(min=5, max=50)])
    password = PasswordField('Пароль', validators=[InputRequired(), Length(min=8, max=50)])
    repeat_password = PasswordField('Повторите пароль', validators=[InputRequired(), EqualTo('password'),
                                                                    Length(min=8, max=50)])
    register = SubmitField('Зарегистрироваться')

    def validate_email(self, field):
        user = Client.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError('На эту почту уже зарегистрирован пользователь')
