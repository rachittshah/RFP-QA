import pytest
import main  # Assuming the file you posted is named "main.py"

@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    with main.app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {"status": "OK"}

def test_upload_file_no_file_part(client):
    response = client.post('/upload')
    assert response.status_code == 400
    assert response.get_json() == {"status": "Failure", "message": "No file part in the request"}

def test_processclaim_no_query(client):
    response = client.post('/docqna')
    assert response.status_code == 400
    assert response.get_json() == {"status": "Failure", "message": "No query provided"}
