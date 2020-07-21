import pytest

from app import app


@pytest.fixture
def client():

    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def validate_token(key, value, json):
    if key in json:
        if json[key] == value:
            return True

    return False

def test_get_profiles_with_valid_credentials_loaded(client):
    """Check if profiles are loaded when credentials are valid"""

    response = client.get("/api/v1/ga/profiles/all")
    assert validate_token('success', True, response.json)


def test_cred_check_is_true(client):
    """Check returns true if credential file is in place"""

    response = client.get("/api/v1/ga/check_cred")
    assert validate_token('success', True, response.json)


test_get_profiles_with_valid_credentials_loaded(app.test_client())