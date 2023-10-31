import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import Token, RefreshToken

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
        "birth_date": "2023-10-31"
    }


@pytest.fixture
def create_user(db, test_user_profile, test_password, test_email):
    def make_user(**kwargs):
        return User.objects.register(
            email=test_email,
            password=test_password,
            profile=test_user_profile
        )
    return make_user


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def get_or_create_token(db, create_user):
    user = create_user()
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


@pytest.mark.django_db
def test_unauthorized_request(api_client):
    url = reverse('users:personal_actions_of_the_client')
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_authorized_request(api_client, get_or_create_token):
    url = reverse('users:personal_actions_of_the_client')
    token = get_or_create_token
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    response = api_client.get(url)
    assert response.status_code == 200
