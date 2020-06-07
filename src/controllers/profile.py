import os
import time
from datetime import datetime

from PIL import Image
from flasgger import swag_from
from flask import Blueprint, render_template, abort, url_for, redirect, request, send_file, jsonify
from flask_login import current_user, login_required
from werkzeug.http import http_date

from database import db
from src.config import Config
from src.controllers.review import is_allowed_to_review
from src.forms.profile.client_profile_edit_form import ClientProfileEditForm
from src.forms.profile.master_profile_edit_form import MasterProfileEditForm
from src.forms.profile.photo_upload_form import PhotoUploadForm
from src.forms.review.review_form import ReviewForm
from src.forms.search.search_form import SearchForm
from src.models import Master
from src.models.client import Client
from src.models.category import Category
from src.models.photo import Photo
from src.models.review import Review
from src.models.service import Service


profile = Blueprint('profile', __name__, template_folder=os.path.join(Config.TEMPLATE_FOLDER, 'profile'),
                    url_prefix='/users')


@profile.route('/<int:id>')
@swag_from('yml/profile_page.yml')
def profile_page(id):
    user = Client.query.get_or_404(id)
    if user.type == 'moderator':  # по идее не требуется так как выше уже сразу client а не user запрашиваетcя
        abort(404)
    users_reviews = user.reviews.join(Client).filter(Client.is_not_blocked.is_(True)).order_by(Review.creation_date.desc())
    reviews_about_master = user.reviews_about_master.join(Client).filter(Client.is_not_blocked.is_(True)).\
        order_by(Review.creation_date.desc()) if user.type == 'master' else None
    page = request.args.get('page', 1, type=int)
    default_author = 'user' if user.type == 'client' else 'others'
    author = request.args.get('author', default_author, type=str)
    users_page = page if author == 'user' else 1
    about_master_page = page if author == 'others' else 1
    users_reviews_pagination = users_reviews.paginate(users_page, Config.REVIEWS_PER_PAGE, True)
    reviews_about_master_pagination = reviews_about_master.paginate(about_master_page, Config.REVIEWS_PER_PAGE, True) \
        if reviews_about_master else None
    reviews_about_master = reviews_about_master_pagination.items if reviews_about_master else []
    # template = 'profile_page.html' # if user.type == 'master' else 'client_profile.html'
    switch_tab_to_users_reviews = user.type == 'master' and author == 'user'
    return render_template('profile_page.html', title=user.name + ' ' + user.surname, search_form=SearchForm(),
                           user=user, review_form=ReviewForm(), allowed_to_review=is_allowed_to_review(user),
                           users_reviews_pagination=users_reviews_pagination,
                           reviews_about_master_pagination=reviews_about_master_pagination,
                           users_reviews=users_reviews_pagination.items, reviews_about_master=reviews_about_master,
                           dont_insert_libraries=True, switch_tab_to_users_reviews=switch_tab_to_users_reviews)


@profile.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@swag_from('yml/profile_edit_get.yml', methods=['GET'])
@swag_from('yml/profile_edit_post.yml', methods=['POST'])
def profile_edit(id):
    user = Client.query.get_or_404(id)
    if user != current_user:
        abort(403)
    if not user.is_not_blocked:
        abort(403)
    if not current_user.email_confirmed:  # нет проверки что не модератор, так как выше уже клиент запрашивается сразу
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


@profile.route('/<int:id>/avatar')
@swag_from('yml/view_avatar.yml')
def avatar(id):
    user = Client.query.get_or_404(id)  # нет проверки что не модератор, так как выше уже клиент запрашивается сразу
    path = user.get_avatar_path()
    if path and os.path.isfile(path):
        return send_file(path)
    else:
        path = os.path.join(Config.UPLOAD_FOLDER, 'default_avatar.jpg')
        return send_file(path)


'''
@profile.after_request
def add_header(response):
    if request.endpoint == 'profile.avatar':
        response.headers['Last-Modified'] = http_date(time.time())
    return response
'''


@profile.route('/photos/<int:id>')
@swag_from('yml/view_photo.yml')
def photo(id):
    photo = Photo.query.get_or_404(id)  # нет проверки что не модератор, так как выше уже клиент запрашивается сразу
    path = photo.get_photo_path()
    if path and os.path.isfile(path):
        return send_file(path)
    abort(404)


@profile.route('/<int:id>/upload-avatar', methods=['GET', 'POST'])
@login_required
@swag_from('yml/upload_avatar_get.yml', methods=['GET'])
@swag_from('yml/upload_avatar_post.yml', methods=['POST'])
def upload_avatar(id):
    photo_form = PhotoUploadForm()  # нет проверки что не модератор, так как выше уже клиент запрашивается сразу
    return upload_image(id, photo_form, avatar=True)


@profile.route('/<int:id>/upload-photo', methods=['GET', 'POST'])
@login_required
@swag_from('yml/upload_photo_get.yml', methods=['GET'])
@swag_from('yml/upload_photo_post.yml', methods=['POST'])
def upload_photo(id):
    photo_form = PhotoUploadForm()  # нет проверки что не модератор, так как выше уже клиент запрашивается сразу
    return upload_image(id, photo_form, avatar=False)


@profile.route('/photos/<int:id>/delete')
@login_required
@swag_from('yml/delete_photo.yml')
def delete_photo(id):
    photo = Photo.query.get_or_404(id)  # нет проверки что не модератор, так как выше уже клиент запрашивается сразу
    master = Master.query.get(photo.master_id)
    if master != current_user:
        abort(403)
    if not current_user.email_confirmed:
        abort(403)
    path = photo.get_photo_path()
    if os.path.isfile(path):
        os.remove(path)
    db.session.delete(photo)
    db.session.commit()
    return redirect(url_for('profile.profile_page', id=master.id))


def upload_image(id, photo_form, avatar=False):
    user = Client.query.get_or_404(id)
    if current_user != user:
        abort(403)
    if not avatar and current_user.type != 'master':
        abort(403)
    if not user.is_not_blocked:
        abort(403)
    if not current_user.email_confirmed:
        abort(403)
    if photo_form.validate_on_submit():
        file = photo_form.photo.data
        if file:
            if upload_image_file(file, user, photo_form, avatar):
                return redirect(url_for('profile.profile_page', id=user.id))
        else:
            photo_form.errors['photo'] = ['Фото не выбрано или имеет запрещённый формат']
    title = 'Изменить фото профиля' if avatar else 'Загрузить фото в галерею'
    return render_template('upload_photo.html',  title=title, photo_form=photo_form)


def upload_image_file(file, user, photo_form, avatar=False):
    folder = user.get_images_folder_path()
    if not os.path.isdir(folder):
        os.mkdir(folder)
    size = sum(entry.stat().st_size for entry in os.scandir(folder)) / 1024 / 1024
    if size > Config.MAX_PHOTOS_SPACE_PER_MASTER:
        photo_form.errors['photo'] = ['Максимальный объём загруженных изображений составляет ' +
                                      str(Config.MAX_PHOTOS_SPACE_PER_MASTER) + ' MB']
        return False
    extension = file.filename.rsplit('.', 1)[1].lower()
    path = os.path.join(folder, 'temp' + '.' + extension)
    file.save(path)
    image = Image.open(path)
    width, height = image.size
    if width > 300 and height > 300:
        if width > height:
            delta = (width - height) / 2
            left = delta
            right = width - delta
            top = 0
            bottom = height
        else:
            delta = (height - width) / 2
            top = delta
            bottom = height - delta
            left = 0
            right = width
        cropped = image.crop((left, top, right, bottom))
        cropped.thumbnail(Config.IMAGES_RESOLUTION, Image.LANCZOS)
        if avatar:
            user.avatar_path = 'avatar' + '.' + extension
            path = os.path.join(folder, 'avatar' + '.' + extension)
        else:
            photo = Photo(master_id=current_user.id)
            db.session.add(photo)
            db.session.commit()
            filename = str(photo.id) + '.' + extension
            photo.path = filename
            path = os.path.join(folder, filename)
        cropped.save(path)
        db.session.commit()
        os.remove(os.path.join(folder, 'temp' + '.' + extension))
        return True
    image.close()
    os.remove(os.path.join(folder, 'temp' + '.' + extension))
    photo_form.errors['photo'] = ['Изображение должно быть хотя бы 300х300 пикселей']
    return False
