import os

from flask import request, redirect, url_for, Blueprint, render_template
from sqlalchemy import func, desc, literal

from src import Config
from src.forms.search.search_filter_form import SearchFilterForm
from src.forms.search.search_form import SearchForm
from src.models.master import Master
from src.models.review import Review
from src.models.service import Service
from src.models.category import Category


search_blueprint = Blueprint('search', __name__, template_folder=os.path.join(Config.TEMPLATE_FOLDER, 'search'))


@search_blueprint.route('/search_', methods=['POST'])
def smart_search():
    search_form = SearchForm()
    query = search_form.query.data.strip()
    if not query:
        return redirect(url_for('search.search'))
    service = Service.query.filter(Service.name.ilike(query)).first()
    if service:
        return redirect(url_for('search.search', query=query, services='s' + str(service.id)))
    category = Category.query.filter(Category.name.ilike(query)).first()
    if category:
        return redirect(url_for('search.search', query=query, services='c' + str(category.id)))
    else:
        master = find_master_by_name(Master.query, "%{}%".format(query), query).first()
        if master:
            return redirect(url_for('search.search', query=query, master=query))
    return redirect(url_for('search.search', query=query))


def find_master_by_name(query, name, reverse_name):
    return query.filter((Master.name + ' ' + Master.surname).ilike(name) |
                        (Master.surname + ' ' + Master.name).ilike(name) |
                        literal(reverse_name).ilike("%" + Master.name + ' ' + Master.surname + "%") |
                        literal(reverse_name).ilike("%" + Master.surname + ' ' + Master.name + "%"))


@search_blueprint.route('/search')
def search():
    search_filter_form = SearchFilterForm(request.args)
    categories_dict = search_filter_form.categories
    search_query = search_filter_form.query.data
    if search_query and not search_filter_form.services.data and not search_filter_form.master.data:
        search_filter_form.query.data = ''
        return render_template('search.html', title='Поиск', search_form=SearchForm(), query=search_query,
                               search_filter_form=search_filter_form, masters=[], categories=categories_dict)
    query = Master.query
    if search_filter_form.master.data:
        name = "%{}%".format(search_filter_form.master.data)
        reverse_name = search_filter_form.master.data
        query = find_master_by_name(query, name, reverse_name)
    services = [int(service[1:]) for service in search_filter_form.services.data if service[0] == 's']
    for service_id in services:
        query = query.filter(Master.services.any(Service.id == service_id))
    categories = [int(category[1:]) for category in search_filter_form.services.data if category[0] == 'c']
    for category_id in categories:
        query = query.filter(Master.services.any(Service.category_id == category_id))
    query = query.filter(Master.is_not_blocked.is_(True))
    if search_filter_form.sort.data == 'rating':
        if search_filter_form.order.data == 'desc':
            query = query.order_by(Master.average_rating.desc())
        else:
            query = query.order_by(Master.average_rating)
    else:
        query = query.outerjoin(Master.reviews_about_master).group_by(Review.master_id)
        if search_filter_form.order.data == 'desc':
            query = query.order_by(desc(func.count(Review.author_id)))
        else:
            query = query.order_by(func.count(Review.author_id))
    if search_filter_form.page.data == '':
        search_filter_form.page.data = '1'
    pagination = query.paginate(int(search_filter_form.page.data), Config.SEARCH_MASTERS_PER_PAGE, True)
    return render_template('search.html', title='Поиск', search_form=SearchForm(), query=search_query,
                           search_filter_form=search_filter_form, masters=pagination.items, pagination=pagination,
                           categories=categories_dict, master_found=search_filter_form.master.data != '',
                           filters=True if search_filter_form.services.data else False)
