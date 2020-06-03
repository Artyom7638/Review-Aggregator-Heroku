from wtforms import TextAreaField, StringField
from wtforms.validators import InputRequired, Length, Optional

from src.forms.phone_number_services_form import PhoneNumberServicesForm
from src.forms.profile.client_profile_edit_form import ClientProfileEditForm


class MasterProfileEditForm(ClientProfileEditForm, PhoneNumberServicesForm):
    short_description = StringField('Краткое описание', validators=[Length(min=10, max=250), Optional()])
    description = TextAreaField('Описание', validators=[Length(min=10, max=2000), Optional()])

    def populate_fields(self, user):
        super().populate_fields(user)
        self.phone_number.data = user.phone_number
        self.short_description.data = user.short_description
        self.description.data = user.description
        self.services.data = [service.id for service in user.services]
