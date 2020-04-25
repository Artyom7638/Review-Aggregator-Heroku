from src.models.user import User


class Moderator(User):

    __mapper_args__ = {
        'polymorphic_identity': 'moderator',
    }
