from flask_wtf import FlaskForm
from wtforms.fields.html5 import TelField
from wtforms.validators import InputRequired, Regexp

from src.models.service import Service
from src.forms.multi_checkbox_field import MultiCheckboxField


class PhoneNumberServicesForm(FlaskForm):
    phone_number = TelField('Телефон', validators=[InputRequired(), Regexp(r"\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}")])
    services = MultiCheckboxField('Услуги', choices=[], coerce=int, validators=[InputRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.services.choices = [(service.id, service.name) for service in Service.query.all()]
