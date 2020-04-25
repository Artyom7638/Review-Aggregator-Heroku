from flask_wtf import FlaskForm
from wtforms import RadioField, HiddenField

from src.models.service import Service
from src.forms.multi_checkbox_field import MultiCheckboxField
from src.models.category import Category


class SearchFilterForm(FlaskForm):
    class Meta:
        csrf = False
    services = MultiCheckboxField('Услуги', choices=[])
    sort = RadioField('Сортировка', choices=[('review_count', 'По количеству отзывов'), ('rating', 'По рейтингу')],
                      default='rating')
    order = RadioField('Порядок', choices=[('asc', 'По возрастанию'), ('desc', 'По убыванию')], default='desc')
    query = HiddenField()
    master = HiddenField()
    page = HiddenField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.services.choices = [('s' + str(service.id), service.name) for service in Service.query.all()]
        categories = [('c' + str(category.id), category.name) for category in Category.query.all()]
        self.services.choices.extend(categories)
