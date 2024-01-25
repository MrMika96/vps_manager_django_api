import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


@pytest.fixture
def test_password():
    return "some_cool_password"


@pytest.fixture
def test_email():
    return "very_coole_email@email.net"


@pytest.fixture
def test_user_profile():
    return {
        "first_name": "john",
        "middle_name": "middlename",
        "last_name": "doe",
        "phone": "+71231231234",
        "birth_date": "2023-10-31",
    }


@pytest.fixture
def create_user(db, test_user_profile, test_password, test_email):
    def make_user(**kwargs):
        return User.objects.register(
            email=test_email, password=test_password, profile=test_user_profile
        )

    return make_user


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, create_user, api_client):
    user = create_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def get_or_create_token(db, create_user):
    user = create_user()
    refresh = RefreshToken.for_user(user)

    return str(refresh), str(refresh.access_token)
