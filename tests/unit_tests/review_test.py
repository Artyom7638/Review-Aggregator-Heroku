from src.models.client import Client
from src.models.review import Review


# Client.is_authenticated = property(lambda self: self.is_authenticated)
current_user = Client(id=1, type='client', is_not_blocked=True, reviews=[])
# current_user.is_authenticated = property(False)
# setattr(current_user, 'is_authenticated', False)
# current_user.is_authenticated = False


def test_review_rights():
    global current_user
    user = Client(id=2, type='client', reviews=[])  # так как в условии and, достаточно проверять по одному условию за раз
    assert not is_allowed_to_review(user, False)  # не is_authenticated
    assert not is_allowed_to_review(user, True)  # is_authenticated, но всё равно нет т.к. не мастер тот
    user.type = 'master'
    assert is_allowed_to_review(user, True)  # теперь мастер
    t = current_user
    current_user = user
    assert not is_allowed_to_review(user, True)  # на самого себя
    current_user = t
    current_user.type = 'moderator'  # модератор не может
    assert not is_allowed_to_review(user, True)
    current_user.type = 'client'
    current_user.is_not_blocked = False  # блокированные не могут
    assert not is_allowed_to_review(user, True)
    current_user.reviews.append(Review(master_id=current_user.id))
    assert not is_allowed_to_review(user, True)  # уже писал отзыв


def is_allowed_to_review(user, is_authenticated):
    if is_authenticated and user.type == 'master' and user != current_user and \
            current_user.type != 'moderator' and current_user.is_not_blocked:
        for r in current_user.reviews:
            if r.master_id == user.id:
                return False
        return True
    return False
