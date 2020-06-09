# -*- coding: utf-8 -*-
from flask import session
from flask_login import login_user, logout_user, current_user
from src.models.master import Master
from src.models.client import Client
from src.models.review import Review


def test_review_rights(test_client, db):
    client = Client.query.filter_by(email='client@client.com').first()
    master = Master.query.filter_by(email='master@master.com').first()
    client_2 = Client.query.filter_by(email='test@test.com').first()
    master_route = '/users/' + str(master.id) + '/review'
    client_route = '/users/' + str(client_2.id) + '/review'

    response = test_client.post(master_route, data=dict(content='test review', rating='5'))
    location = [h for h in response.headers if h[0] == 'Location'][0][1]  # value это второе в tuple, поэтому 1
    assert response.status_code == 302 and 'login' in location  # не is_authenticated

    response = test_client.post('/login', data=dict(email=client.email, password='test_password'))
    response = test_client.post(client_route, data=dict(content='test review', rating='5'))
    assert response.status_code == 404  # is_authenticated, но всё равно нет т.к. не мастер
    response = test_client.post(master_route, data=dict(content='test review', rating='5'))
    assert response.status_code == 302  # теперь мастер
    db.session.delete(client.reviews[0])
    db.session.commit()
    response = test_client.get('/logout', data=dict(email=master.email, password='test_password'))
    response = test_client.post('/login', data=dict(email=master.email, password='test_password'))
    print(current_user.id)
    print(master.id)
    response = test_client.post(master_route, data=dict(content='test review', rating='5'))
    print(current_user.is_authenticated)
    print(current_user.id)
    print(master.id)
    assert response.status_code == 403  # на самого себя
    print(current_user.is_authenticated)
    response = test_client.get('/logout', data=dict(email=master.email, password='test_password'))
    print(current_user.is_authenticated)

    response = test_client.post('/login', data=dict(email=client.email, password='test_password'))
    print(current_user.id)
    print(current_user.is_authenticated)
    client.type = 'moderator'  # модератор не может
    db.session.commit()
    response = test_client.post(master_route, data=dict(content='test review', rating='5'))
    assert response.status_code == 403
    client.type = 'client'
    db.session.commit()
    client.is_not_blocked = False  # блокированные не могут
    db.session.commit()
    print(current_user.id)
    print(current_user.is_authenticated)
    response = test_client.post(master_route, data=dict(content='test review', rating='5'))
    assert response.status_code == 403
    client.is_not_blocked = True  # блокированные не могут
    client.email_confirmed = False
    db.session.commit()
    print(current_user.id)
    print(current_user.is_authenticated)
    response = test_client.post(master_route, data=dict(content='test review', rating='5'))
    assert response.status_code == 403

    client.reviews.append(Review(master_id=master.id))
    db.session.commit()
    response = test_client.post(master_route, data=dict(content='test review', rating='5'))
    assert response.status_code == 403  # уже писал отзыв
