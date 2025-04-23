import pytest
from flask import Flask
import sys
sys.path.insert(0, '.')  # Add root directory to path
from app import app
 

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client
def test_quiz_endpoint(client):
    response = client.get('/quiz')      # check endpoind /quiz

    assert response.status_code == 200
    data = response.get_json()
    assert 'quiz' in data           # check 'quiz' key exists 

    assert isinstance(data['quiz'], list)  # Ensure 'quiz' is a list

    assert len(data['quiz']) == 15      # check exactly 15 questions