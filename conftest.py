import pytest
from rest_framework.test import APIClient

from user_management.tests.factories import UserFactory

@pytest.fixture
def api_client():
    client = APIClient()
    user = UserFactory()
    client.force_authenticate(user=user)
    return client
