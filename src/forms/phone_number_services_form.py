from flask_wtf import FlaskForm
from wtforms.fields.html5 import TelField
from wtforms.validators import InputRequired, Length

from src.models.service import Service
from src.forms.multi_checkbox_field import MultiCheckboxField


class PhoneNumberServicesForm(FlaskForm):
    phone_number = TelField('Телефон', validators=[InputRequired()])
    services = MultiCheckboxField('Услуги', choices=[], coerce=int, validators=[InputRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.services.choices = [(service.id, service.name) for service in Service.query.all()]
