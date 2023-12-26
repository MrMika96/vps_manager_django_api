import pytest
from django.urls import reverse

from applications.models import Application
from users.models import User


@pytest.mark.django_db
def test_application_list_request(api_client_with_credentials):
    url = reverse('applications:applications-list')
    response = api_client_with_credentials.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_application_detail_request(api_client_with_credentials):
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
    some_application = Application.objects.create(
        title='test',
        deployer=some_user,
        size=100
    )
    url = reverse('applications:applications-detail', args=[some_application.id])
    response = api_client_with_credentials.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_application_update_request(api_client_with_credentials, test_password):
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

    some_application = Application.objects.create(
        title='test',
        deployer=some_user,
        size=100
    )

    url = reverse('applications:applications-detail', args=[some_application.id])

    response = api_client_with_credentials.put(
        url,
        data={
            "title": "test",
            "size": 100,
            "deployed_to": []
        },
        format="json"
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_application_delete_request(api_client_with_credentials, test_password):
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

    some_application = Application.objects.create(
        title='test',
        deployer=some_user,
        size=100
    )

    url = reverse('applications:applications-detail', args=[some_application.id])

    response = api_client_with_credentials.delete(url)

    assert response.status_code == 204


@pytest.mark.django_db
def test_application_create_request(api_client_with_credentials):
    url = reverse('applications:applications-list')

    response = api_client_with_credentials.post(
        url,
        data={
            "title": "test",
            "size": 100,
            "deployed_to": []
        },
        format="json"
    )

    assert response.status_code == 201
