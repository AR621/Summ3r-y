import pytest
from summ3ry.app import app


@pytest.fixture
def app_():
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app_):
    return app_.test_client()


def test_home_page(client):
    response = client.get()
    assert response.status_code == 200


def test_about(client):
    response = client.get('/about')
    assert response.status_code == 200
    

def test_example(client):
    response = client.get('/example')
    assert response.status_code == 200
    
    
def test_upload_buttons(client):
    response = client.post('/')
    assert response.status_code == 200
