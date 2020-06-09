from flask_login import current_user, logout_user


def test_login(test_client):
    response = test_client.post('/login', data=dict(email='wrong@wrong.com', password='wrong'))
    assert response.status_code == 200 and not current_user.is_authenticated
    response = test_client.post('/login', data=dict(email='test@test.com', password='wrong'))
    assert response.status_code == 200 and not current_user.is_authenticated
    response = test_client.post('/login', data=dict(email='wrong@wrong.com', password='test_password'))
    assert response.status_code == 200 and not current_user.is_authenticated
    response = test_client.post('/login', data=dict(email='test@test.com', password='test_password'))
    assert response.status_code == 302 and current_user.is_authenticated
    logout_user()
    assert not current_user.is_authenticated
