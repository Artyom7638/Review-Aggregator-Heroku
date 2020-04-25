from wtforms import SubmitField, StringField
from wtforms.validators import InputRequired, Length

from src.forms.name_surname_form import NameSurnameForm


class ClientProfileEditForm(NameSurnameForm):
    edit = SubmitField('Сохранить')

    def populate_fields(self, user):
        self.name.data = user.name
        self.surname.data = user.surname
