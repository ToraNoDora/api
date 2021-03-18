import pytest
from app import *


@pytest.fixture
def client():
    with app.test_client() as client:

        yield client


# Функции для упрощения тестов
def last_id():
    last_id = notes[-1]['id']
    return last_id


def json_comparison(data, json):
    print(data, json)
    assert data['title'] == json['title']
    assert data['text'] == json['text']
    assert data['tags'] == json['tags']


# Тесты
def test_get_notes(client):
    r = client.get('/notes/api/notes')
    
    assert r.get_json()[0]['id'] == 1
    assert r.status_code == 200
    

def test_create_note(client):
    data = {
        'title': 'Test title',
        'text': 'Test text', 
        'tags': ['tag10', 'tag20', 'tag30']
    }
    
    r = client.post('/notes/api/notes', json=data)

    json_comparison(data, r.get_json())
    assert 'id' in r.get_json()
    assert r.status_code == 201


def test_get_note(client):
    r = client.get('/notes/api/notes/{}'.format(last_id()))
    
    assert r.status_code == 200


def test_update_note(client):
    data = {
        'title': 'New test title',
        'text': 'New text', 
        'tags': ['tag1', 'tag2', 'tag4']
    }
    
    r = client.put('/notes/api/notes/{}'.format(last_id()), json=data)

    json_comparison(data, r.get_json())
    assert r.status_code == 200


def test_delete_note(client):
    r = client.delete('/notes/api/notes/{}'.format(last_id()))
    
    assert r.status_code == 200
    assert r.get_json()['result'] == True
    

    