from flask import Blueprint, abort, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func

from database import db
from src.config import Config
from src.models import Master
from src.models.client import Client
from src.models.review import Review

moderator = Blueprint('moderator', __name__)


@moderator.route('/review/<int:id>/delete')
@login_required
def delete_review(id):
    if current_user.type != 'moderator':
        abort(403)
    review = Review.query.get_or_404(id)
    master_id = review.master_id
    db.session.delete(review)
    master = Master.query.get(master_id)
    if master.reviews_about_master.count() >= Config.MIN_AMOUNT_OF_REVIEWS_FOR_RATING:
        master.average_rating = db.session.query(func.avg(Review.rating)).filter_by(master_id=master.id).scalar()
    else:
        master.average_rating = None
    db.session.commit()
    return redirect(url_for('profile.profile_page', id=master_id))


@moderator.route('/user/<int:id>/block')
@login_required
def block_user(id):
    if current_user.type != 'moderator':
        abort(403)
    user = Client.query.get_or_404(id)
    user.is_not_blocked = False
    db.session.commit()
    return redirect(url_for('profile.profile_page', id=user.id))
