from wtforms.fields.html5 import TelField
from wtforms.validators import InputRequired

from src.forms.auth.client_registration_form import ClientRegistrationForm
from src.forms.multi_checkbox_field import MultiCheckboxField
from src.forms.phone_number_services_form import PhoneNumberServicesForm
from src.models.service import Service


class MasterRegistrationForm(ClientRegistrationForm, PhoneNumberServicesForm):
    pass
