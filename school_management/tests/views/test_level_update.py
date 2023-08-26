import pytest
from django.urls import reverse
from rest_framework import status

from school_management.tests.factories import LevelFactory


@pytest.mark.django_db
@pytest.mark.views
def test_level_update(api_client):
    level = LevelFactory()
    old_name = level.name

    # Prepare new data
    new_name = "Updated Level Name"
    data = {
        "name": new_name
    }

    # URL for the API endpoint
    url = reverse('level-update', kwargs={'pk': level.pk})

    # Perform the API call
    response = api_client.put(url, data)

    # Check HTTP status
    assert response.status_code == status.HTTP_200_OK

    # Refresh the instance from the DB and check if it's updated
    level.refresh_from_db()
    assert level.name == new_name
    assert level.name != old_name


@pytest.mark.django_db
@pytest.mark.views
def test_level_update_bad_request(api_client):
    level = LevelFactory()

    # Prepare bad data
    data = {
        "name": "",
    }

    url = reverse('level-update', kwargs={'pk': level.pk})
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data  # Check that 'name' field is in the errors
    assert response.data['name'][0] == 'Name cannot be empty.'  # Custom error message
