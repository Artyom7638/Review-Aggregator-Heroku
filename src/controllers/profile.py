import os

from flask import Blueprint, render_template, abort, url_for, redirect, request
from flask_login import current_user, login_required


from database import db
from src import Config
from src.controllers.review import is_allowed_to_review
from src.forms.profile.client_profile_edit_form import ClientProfileEditForm
from src.forms.profile.master_profile_edit_form import MasterProfileEditForm
from src.forms.review.review_form import ReviewForm
from src.forms.search.search_form import SearchForm
from src.models.client import Client
from src.models.category import Category
from src.models.review import Review
from src.models.service import Service

profile = Blueprint('profile', __name__, template_folder=os.path.join(Config.TEMPLATE_FOLDER, 'profile'),
                    url_prefix='/users')


@profile.route('/<int:id>')
def profile_page(id):
    user = Client.query.get_or_404(id)
    if user.type == 'moderator':
        abort(404)
    users_reviews = user.reviews.order_by(Review.creation_date.desc())
    reviews_about_master = user.reviews_about_master.order_by(Review.creation_date.desc()) \
        if user.type == 'master' else None
    page = request.args.get('page', 1, type=int)
    default_author = 'user' if user.type == 'client' else 'others'
    author = request.args.get('author', default_author, type=str)
    users_page = page if author == 'user' else 1
    about_master_page = page if author == 'others' else 1
    users_reviews_pagination = users_reviews.paginate(users_page, Config.REVIEWS_PER_PAGE, True)
    reviews_about_master_pagination = reviews_about_master.paginate(about_master_page, Config.REVIEWS_PER_PAGE, True) \
        if reviews_about_master else None
    reviews_about_master = reviews_about_master_pagination.items if reviews_about_master else None
    return render_template('profile_page.html', title=user.name + ' ' + user.surname, search_form=SearchForm(),
                           user=user, review_form=ReviewForm(), allowed_to_review=is_allowed_to_review(user),
                           users_reviews_pagination=users_reviews_pagination,
                           reviews_about_master_pagination=reviews_about_master_pagination,
                           users_reviews=users_reviews_pagination.items, reviews_about_master=reviews_about_master)


@profile.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def profile_edit(id):
    user = Client.query.get_or_404(id)
    if user != current_user:
        abort(403)
    if user.type == 'master':
        edit_form = MasterProfileEditForm()
        template = 'master_profile_edit.html'
    else:
        edit_form = ClientProfileEditForm()
        template = 'client_profile_edit.html'
    if edit_form.validate_on_submit():
        user.name = edit_form.name.data
        user.surname = edit_form.surname.data
        if user.type == 'master':
            user.phone_number = edit_form.phone_number.data
            user.short_description = edit_form.short_description.data
            user.description = edit_form.description.data
            user.services = Service.query.filter(Service.id.in_(edit_form.services.data)).all()
        db.session.commit()
        return redirect(url_for('profile.profile_page', id=user.id))
    if request.method == 'GET':
        edit_form.populate_fields(user)
    categories = {category.name: category for category in Category.query.all()}
    return render_template(template, title='Редактирование профиля', search_form=SearchForm(), edit_form=edit_form,
                           categories=categories)


