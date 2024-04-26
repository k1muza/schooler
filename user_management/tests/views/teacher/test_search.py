from django.http import QueryDict
import pytest
from django.urls import reverse
from rest_framework import status

from user_management.tests.factories import TeacherFactory, UserFactory

@pytest.mark.parametrize("search_term, result_count", [
    ('John', 1),
    ('Doe', 2),
    ('alice123', 1),
    ('bob@email.com', 1),
    ('no-match', 0)
])
@pytest.mark.django_db
@pytest.mark.views
def test_teacher_search_by_admin(superuser_client, search_term, result_count):
    client, _ = superuser_client
    # Create sample Teacher instances with different attributes
    TeacherFactory(user=UserFactory(first_name="John", last_name="Doe"))
    TeacherFactory(user=UserFactory(first_name="Jane", last_name="Doe"))
    TeacherFactory(user=UserFactory(first_name="Alice", username="alice123"))
    TeacherFactory(user=UserFactory(first_name="Bob", email="bob@email.com"))

    # Test search by first_name
    params = QueryDict(mutable=True)
    params['search'] = search_term
    query_string = params.urlencode()
    url = reverse('teacher-search') + '?' + query_string

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == result_count
