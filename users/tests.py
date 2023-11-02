import pytest
from django.urls import reverse
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
def api_client_with_credentials(
        db, create_user, api_client
):
    user = create_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def get_or_create_token(db, create_user):
    user = create_user()
    refresh = RefreshToken.for_user(user)
    return str(refresh), str(refresh.access_token)


@pytest.mark.django_db
def test_unauthorized_request(api_client):
    url = reverse('users:user_personal_data')
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_authorized_with_token_request(api_client, get_or_create_token):
    url = reverse('users:user_personal_data')
    refresh_token, access_token = get_or_create_token
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_receive_personal_data_request(api_client_with_credentials):
    url = reverse('users:user_personal_data')
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_personal_data_request(api_client_with_credentials, test_user_profile):
    url = reverse('users:user_personal_data')
    response = api_client_with_credentials.put(
        url,
        data={"profile": test_user_profile},
        format="json"
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_personal_data_request(api_client_with_credentials):
    url = reverse('users:user_personal_data')
    response = api_client_with_credentials.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_change_credentials_request(api_client_with_credentials, test_password):
    url = reverse('users:user-change_credentials')
    response = api_client_with_credentials.put(
        url,
        data={
            "email": "cool_new_email@cmail.com",
            "password": "some_new_very_cool_password",
            "old_password": test_password
        },
        format="json"
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_registration_request(api_client, test_user_profile, test_password, test_email):
    url = reverse("users:user-register")
    response = api_client.post(
        url,
        data={
            "email": test_email,
            "password": test_password,
            "profile": test_user_profile
        },
        format="json"
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_user_auth_request(api_client, create_user, test_password):
    url = reverse("users:user_auth")
    user = create_user()
    response = api_client.post(
        url,
        data={
            "email": user.email,
            "password": test_password
        },
        format="json"
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_users_list_request(api_client_with_credentials):
    url = reverse('users:user-list')
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_detail_request(api_client_with_credentials, create_user):
    some_user = User.objects.register(
            email="some_lame_email@booo.me",
            password="12334",
            profile={
                "first_name": "very",
                "middle_name": "lame",
                "last_name": "dude",
                "phone": "+71231231123",
                "birth_date": "2023-10-31"
    }
        )
    url = reverse('users:user-detail', args=[some_user.id])
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_auth_refresh(client, get_or_create_token):
    refresh_token, access_token = get_or_create_token
    print(refresh_token),
    print(access_token)
    url = reverse('users:user_auth_refresh')
    response = client.post(url, data={'refresh': refresh_token})
    assert response.status_code == 200
