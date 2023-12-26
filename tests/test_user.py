import pytest
from django.urls import reverse

from users.models import User


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
    url = reverse('users:user_auth_refresh')
    response = client.post(url, data={'refresh': refresh_token})

    assert response.status_code == 200
