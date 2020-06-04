from src.forms.auth.client_registration_form import ClientRegistrationForm
from src.forms.phone_number_services_form import PhoneNumberServicesForm


class MasterRegistrationForm(ClientRegistrationForm, PhoneNumberServicesForm):
    pass
