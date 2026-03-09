import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.get_db_connection')
def test_get_tasks(mock_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    response = client.get('/tasks')
    assert response.status_code == 200

@patch('app.get_db_connection')
def test_create_task(mock_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1, 'Test Task', 'Description', 'pending', None)
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    response = client.post('/tasks', json={
        'title': 'Test Task',
        'description': 'Description'
    })
    assert response.status_code == 201

@patch('app.get_db_connection')
def test_get_task_not_found(mock_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    response = client.get('/tasks/999')
    assert response.status_code == 404