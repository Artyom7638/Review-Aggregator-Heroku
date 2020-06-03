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
        choices = []
        c = {}
        i = 0
        for cat in Category.query.all():
            selected = True if self.services.data and 'c' + str(cat.id) in self.services.data else False
            l = [{'name': cat.name, 'val': 'c' + str(cat.id), 'id': self.services.name + '-' + str(i),
                  'selected': selected}]
            choices.append(('c' + str(cat.id), cat.name))
            i += 1
            for service in cat.services:
                selected = True if self.services.data and 's' + str(service.id) in self.services.data else False
                l.append({'name': service.name, 'val': 's' + str(service.id), 'id': self.services.name + '-' + str(i),
                          'selected': selected})
                choices.append(('s' + str(service.id), service.name))
                i += 1
            c[cat.name] = l
        self.services.choices = choices
        self.categories = c
