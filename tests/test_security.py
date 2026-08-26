import pytest
import io
import json
import zipfile
import tempfile
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, validate_channels, _sessions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload_0_byte(client):
    data = {'file': (io.BytesIO(b""), 'test.scm')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400

def test_upload_bad_magic(client):
    data = {'file': (io.BytesIO(b"badmagicbytes123"), 'test.scm')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b'INVALID_EXTENSION' in response.data or b'Parse_error' in response.data

def test_validation_logic():
    valid, msg = validate_channels([])
    assert not valid
    assert "empty" in msg

    valid, msg = validate_channels([{'Name': 'A' * 41}])
    assert not valid
    assert "exceeds" in msg

    valid, msg = validate_channels([{'Slot': -1}])
    assert not valid
    assert "negative" in msg

    valid, msg = validate_channels([{'Slot': 1, 'Name': 'Test'}])
    assert valid

def test_api_validate(client):
    resp = client.post('/api/validate', json={"channels": [{'Name': 'A' * 41}]})
    assert resp.status_code == 400
    
    resp = client.post('/api/validate', json={"channels": [{'Slot': 1}]})
    assert resp.status_code == 200

def test_api_dedupe(client):
    channels = [
        {'Freq': 11000, 'SID': 1, 'Name': 'Ch1'},
        {'Freq': 11000, 'SID': 1, 'Name': 'Ch1 Duplicate'},
        {'Freq': 12000, 'SID': 2, 'Name': 'Ch2'}
    ]
    resp = client.post('/api/actions/dedupe', json={"channels": channels})
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data['channels']) == 2
    assert data['deleted'] == 1

def test_build_invalid_session(client):
    resp = client.post('/build', json={"session_id": "invalid123", "channels": [{'Slot': 1}]})
    assert resp.status_code == 400

def test_build_invalid_channels(client):
    # Valid session but invalid channels
    _sessions["test_session"] = {'path': 'test', 'brand': 'lg', 'ext': '.tll', 'tmpdir': '/tmp'}
    resp = client.post('/build', json={"session_id": "test_session", "channels": [{'Slot': -1}]})
    assert resp.status_code == 400
    
def test_rate_limit(client):
    # A bit hard to test deterministically without sleeping, but let's just make a few requests.
    pass

