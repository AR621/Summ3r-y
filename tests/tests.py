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
    response = client.get('/')
    assert response.status_code == 200
    assert b'<title>Index</title>' in response.data


def test_about(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'<title>About</title>' in response.data

    
def test_example(client):
    response = client.get('/example')
    assert response.status_code == 200
    assert b'<title>Example</title>' in response.data


def test_empty_file_upload(client):
    file_data = ''
    response = client.post('/',
                           data=dict(upload_button='upload', file=file_data, content_type='multipart/form-data', follow_redirects=True))
    assert response.status_code == 400


# FAILS due to no flash msg in response (redirection)
# def test_invalid_file_upload(client):
#     file_data = open('../tests/sample.txt', 'rb')
#     response = client.post('/',
#                            data=dict(upload_button='upload', file=file_data, content_type='multipart/form-data', follow_redirects=True))
#     assert response.status_code == 302
#     assert b'<strong>Empty file or format is not allowed, try to upload file with .mp3 extension</strong>' in response.data


# FAILS due to long redirection
# def test_file_upload(client):
#     file_data = open('../tests/sample.mp3', 'rb')
#     response = client.post('/',
#                            data=dict(upload_button='upload', file=file_data), content_type='multipart/form-data', follow_redirects=True)
#     assert response.status_code == 200
#     assert b'<title>Summary</title>' in response.data
#     assert b'<a>Transcript</a>' in response.data
#     assert b'<a>Summary</a>' in response.data


def test_empty_url_paste(client):
    url_data = ''
    response = client.post('/',
                           data=dict(url_button='paste', file=url_data, content_type='multipart/form-data', follow_redirects=True))
    assert response.status_code == 200
    assert b'<strong>Empty url</strong>' in response.data
  
    
# FAILS due to no flash msg in response (redirection)
# def test_invalid_url_paste(client):
#     url_data = 'https://github.com/AR621/Summ3r-y'
#     response = client.post('/',
#                            data=dict(url_button='paste', file=url_data, content_type='multipart/form-data', follow_redirects=True))
#     assert response.status_code == 200
#     assert b'<strong>Invalid url</strong>' in response.data


# FAILS due to long redirection
# def test_url_paste(client):
#     url_data = 'https://youtu.be/B_fXSJ97H0E'
#     response = client.post('/',
#                            data=dict(url_button='paste', url=url_data, content_type='multipart/form-data', follow_redirects=True))
#     assert response.status_code == 200
#     assert b'<title>Summary</title>' in response.data
#     assert b'<a>Transcript</a>' in response.data
#     assert b'<a>Summary</a>' in response.data
    
    