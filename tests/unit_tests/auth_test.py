from src.models.client import Client


def test_login():
    user = Client(email='test@test.com')
    password = 'test_password'
    user.set_password(password)
    assert user.check_password(password)
    assert not test_login_attempt(user, 'wrong@wrong.com', 'wrong')
    assert not test_login_attempt(user, user.email, 'wrong')
    assert not test_login_attempt(user, 'wrong@wrong.com', 'test_password')
    assert test_login_attempt(user, user.email, 'test_password')


def test_login_attempt(user, login_input, password_input):
    try:
        assert user.email == login_input
        assert user.check_password(password_input) is True
    except AssertionError:
        return False
    return True
