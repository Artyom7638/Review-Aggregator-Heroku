from flask import Blueprint, abort, url_for, redirect, flash
from flask_login import login_required, current_user
from sqlalchemy import func

from database import db
from src import Config
from src.forms.review.review_form import ReviewForm
from src.models.client import Client
from src.models.review import Review
from src.models.user import User

review = Blueprint('review', __name__,)


@review.route('/users/<int:id>/review', methods=['POST'])
@login_required
def post_review(id):
    user = User.query.get_or_404(id)
    allowed_to_review = is_allowed_to_review(user)
    if not allowed_to_review:
        abort(403)
    review_form = ReviewForm()
    if review_form.validate_on_submit():
        review = Review(content=review_form.content.data, rating=review_form.rating.data, author_id=current_user.id,
                        master_id=id)
        db.session.add(review)
        if user.reviews_about_master.count() >= Config.MIN_AMOUNT_OF_REVIEWS_FOR_RATING:
            user.average_rating = db.session.query(func.avg(Review.rating)).filter_by(master_id=user.id).scalar()
        db.session.commit()
        flash('Ваш отзыв успешно сохранён', 'success')
    else:
        for field, error_list in review_form.errors.items():
            for error in error_list:
                flash(review_form[field].label.text + ': ' + error, 'error')
    return redirect(url_for('profile.profile_page', id=id))


def is_allowed_to_review(user):
    if current_user.is_authenticated and user.type == 'master' \
            and user != current_user and current_user.type != 'moderator':
        return current_user.reviews.filter(Review.master_id == user.id).first() is None
    return False
