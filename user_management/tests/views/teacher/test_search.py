import pytest
from django.urls import reverse
from rest_framework import status

from user_management.tests.factories import TeacherFactory, UserFactory

@pytest.mark.django_db
@pytest.mark.views
def test_teacher_search(api_client):
    # Create sample Teacher instances with different attributes
    TeacherFactory(user=UserFactory(first_name="John", last_name="Doe"))
    TeacherFactory(user=UserFactory(first_name="Jane", last_name="Doe"))
    TeacherFactory(user=UserFactory(first_name="Alice", username="alice123"))
    TeacherFactory(user=UserFactory(first_name="Bob", email="bob@email.com"))

    # Test search by first_name
    url = reverse('teacher-search', kwargs={'search': 'John'})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1  # Should return one match

    # Test search by last_name
    url = reverse('teacher-search', kwargs={'search': 'Doe'})
    response = api_client.get(url)
    assert len(response.data) == 2  # Should return two matches

    # Test search by username
    url = reverse('teacher-search', kwargs={'search': 'alice123'})
    response = api_client.get(url)
    assert len(response.data) == 1

    # Test search by email
    url = reverse('teacher-search', kwargs={'search': 'bob@email.com'})
    response = api_client.get(url)
    assert len(response.data) == 1

    # Test no matches
    url = reverse('teacher-search', kwargs={'search': 'no-match'})
    response = api_client.get(url)
    assert len(response.data) == 0

