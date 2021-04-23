import pytest
from app.app import *


@pytest.fixture
def client():
    with app.test_client() as client:

        yield client

# Функции для упрощения тестов
def last_id():
    query = Note.select()
    q = []
    for i in query:
        n = model_to_dict(i)
        q.append(n)
    q_2 = q[-1]
    last_id = q_2['id']

    return last_id

def three_id():
    query = Note.select()
    q = []
    for i in query:
        n = model_to_dict(i)
        q.append(n)
    q_2 = q[2]
    three = q_2['id']

    return three_id


# ТЕСТЫ
def test_get_notes(client):
    r = client.get('/notes')
    
    assert r.status_code == 200

# Тест на одинаковые и новые теги при создании записи
def test_create_note_tag(client):
    data = {
        'title': 'Test create some tags',
        'text': 'Test some tags', 
        'tags': ['dfgd', 'some', 'new', 'cat']
    }
    
    r = client.post('/notes', json=data)
    
    assert r.status_code == 201

# Тест только на новые теги при создании записи
def test_create_note(client):
    data = {
        'title': 'Test title',
        'text': 'Test text', 
        'tags': ['trr', 'rtrtr', 'kjlj']
    }
    
    r = client.post('/notes', json=data)

    
    assert r.status_code == 201


def test_get_note(client):
    r = client.get('/notes/{}'.format(last_id()))
    
    assert r.status_code == 200

# Тест только на новые теги при изменении записи
def test_update_note(client):
    data = {
        'title': 'New test iiii',
        'text': 'New text iiiii', 
        'tags': ['iiii', 'iiiii', 'iiiii']
    }
    
    r = client.put('/notes/{}'.format(last_id()), json=data)

    
    assert r.status_code == 200


def test_delete_note(client):
    r = client.delete('/notes/{}'.format(last_id()))
    
    assert r.status_code == 200
    assert r.get_json()['result'] == True
    
# Тест на одинаковые и новые теги при изменении записи
def test_update_note(client):
    data = {
        'title': 'New test title',
        'text': 'New text', 
        'tags': ['little tag', 'sup', 'bbbb', 'aaaa']
    }
    
    r = client.put('notes/{}'.format(three_id()), json=data)

    assert r.status_code == 200