from src.models.master import Master


def test_search(test_client, db):
    master_1 = Master.query.filter_by(surname='Иванова').first()
    master_2 = Master.query.filter_by(surname='Петрова').first()
    master_3 = Master.query.filter_by(surname='Бородина').first()
    m1 = master_1.name + ' ' + master_1.surname
    m2 = master_2.name + ' ' + master_2.surname
    m3 = master_3.name + ' ' + master_3.surname
    response = test_client.post('search_', data=dict(query='Ольга'), follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200 and m1 in data and m2 in data
    response = test_client.post('search_', data=dict(query='ольга'), follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200 and m1 in data and m2 in data
    response = test_client.post('search_', data=dict(query='Иванова'), follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200 and m1 in data
    response = test_client.post('search_', data=dict(query='иванова'), follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200 and m1 in data
    response = test_client.post('search_', data=dict(query='Ольга'), follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200 and m1 in data and m2 in data

    assert response.status_code == 200 and m1 in data
    response = test_client.post('search_', data=dict(query='Ольга Петрова'), follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200 and m2 in data
    response = test_client.post('search_', data=dict(query='ольга петрова'), follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200 and m2 in data

    assert response.status_code == 200 and m1 in data
    response = test_client.post('search_', data=dict(query='Петрова Ольга'), follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200 and m2 in data
    response = test_client.post('search_', data=dict(query='петрова ольга'), follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200 and m2 in data

    assert response.status_code == 200 and m1 in data
    response = test_client.post('search_', data=dict(query='Окрашивание'), follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200 and m1 in data
    response = test_client.post('search_', data=dict(query='окрашивание'), follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200 and m1 in data

    assert response.status_code == 200 and m1 in data
    response = test_client.post('search_', data=dict(query='Пирсинг'), follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200 and m3 in data
    response = test_client.post('search_', data=dict(query='пирсинг'), follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200 and m3 in data

    assert response.status_code == 200 and m1 in data
    response = test_client.post('search_', data=dict(query='Цветные татуировки'), follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200 and m2 in data and m3 in data
    response = test_client.post('search_', data=dict(query='test'), follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200 and m1 not in data and m2 not in data and m3 not in data
    response = test_client.post('search_', data=dict(query='Test Test'), follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200 and m1 not in data and m2 not in data and m3 not in data
