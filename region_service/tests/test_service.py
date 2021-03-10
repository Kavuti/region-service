import os
import pytest
from .. import create_app, db
from ..model.region import Region
from flask import Response as BaseResponse, json
from flask.testing import FlaskClient
from werkzeug.utils import cached_property

@pytest.fixture(scope="session")
def app():
    class Response(BaseResponse):
        @cached_property
        def json(self):
            return json.loads(self.data)

    class TestClient(FlaskClient):
        def open(self, *args, **kwargs):
            if 'json' in kwargs:
                kwargs['data'] = json.dumps(kwargs.pop('json'))
                kwargs['content_type'] = 'application/json'
            return super(TestClient, self).open(*args, **kwargs)

    _app = create_app(True)
    _app.response_class = Response
    _app.test_client_class = TestClient
    return _app

@pytest.fixture
def test_db():
    return db

@pytest.fixture
def client(app):
    _client = app.test_client()
    return _client
    
@pytest.fixture(scope="session")
def fake_region(test_db):
    _fake_region = Region()
    _fake_region.description = 'Northern Fake'
    test_db.session.add(_fake_region)
    test_db.session.commit()
    return _fake_region
    

def test_get_all_regions(client):
    res = client.get('/regions')
    assert res.status_code == 200
    assert type(res.json['data']) == list
    assert res.headers['Content-Type'] == 'application/json'

def test_get_region(client, fake_region):
    res = client.get(f"/regions?id={fake_region.id}")
    assert res.status_code == 200
    assert res.headers['Content-Type'] == 'application/json'
    assert type(res.json['data']) == dict
    assert res.json['data']['id'] == fake_region.id
    assert res.json['data']['description'] == fake_region.description
    
def test_create_region(client):
    valid_region = {'description': 'New Fake Region'}
    res = client.post("/regions", json=valid_region)
    assert res.status_code == 200
    assert res.headers['Content-Type'] == 'application/json'
    assert type(res.json['data']) == dict
    assert res.json['data']['id'] != None
    assert res.json['data']['description'] == valid_region['description']
    assert res.json['data']['active'] == True


def test_update_region(client, fake_region):
    update_payload = {'description': 'Updated Fake'}
    res = client.put(f"/regions?id={fake_region.id}", data=update_payload)
    assert res.status_code == 200
    assert res.headers['Content-Type'] == 'application/json'
    assert type(res.json['data']) == dict
    assert res.json['data']['id'] == fake_region.id
    assert res.json['data']['description'] == update_payload['description']


def test_delete_region(client, fake_region):
    res = client.delete(f"/regions?id={fake_region.id}")
    assert res.status_code == 200
    assert res.headers['Content-Type'] == 'application/json'
    assert type(res.json['data']) == bool
    assert res.json['data'] == True
    
    get_res = client.get(f"/regions?id?{fake_region.id}")
    assert res.status_code == 200
    assert res.headers['Content-Type'] == 'application/json'
    assert type(res.json['data']) == dict
    assert res.json['data'] == {}
    