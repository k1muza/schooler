import pytest
from rest_framework import status
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.views
def test_level_create(user_client):
    client, _ = user_client
    data = {
        'name': 'New Level'
    }
    url = reverse('level-create')
    response = client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.data 


@pytest.mark.django_db
@pytest.mark.views
def test_level_create_invalid_name(user_client):
    client, _ = user_client
    data = {
        'name': '',
    }
    url = reverse('level-create')
    response = client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Name cannot be empty.' in str(response.data)
