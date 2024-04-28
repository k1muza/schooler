from django.http import QueryDict
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user_management.tests.factories import TeacherFactory, UserFactory

data = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
    },
    {
        "first_name": "Jane",
        "last_name": "Doe",
        "username": "janedoe",
    },
    {
        "first_name": "Alice",
        "username": "alice123",
    },
    {
        "first_name": "Bob",
        "email": "bob@email.com"
    }
]

@pytest.fixture
@pytest.mark.django_db
def teacher_data():
    for kwargs in data:
        TeacherFactory(user=UserFactory(**kwargs))


@pytest.mark.parametrize("search_term, result_count", [
    ('John', 1),
    ('Doe', 2),
    ('alice123', 1),
    ('bob@email.com', 1),
    ('no-match', 0)
])
@pytest.mark.django_db
@pytest.mark.views
def test_teacher_search_by_admin(superuser_client, teacher_data, search_term, result_count):
    client, _ = superuser_client

    # Test search by first_name
    params = QueryDict(mutable=True)
    params['search'] = search_term
    query_string = params.urlencode()
    url = reverse('teacher-search') + '?' + query_string

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == result_count


@pytest.mark.django_db
def test_teacher_search_by_schooladmin(administrator_client):
    pass


@pytest.mark.django_db
def test_teacher_search_by_self(teacher_client):
    pass


@pytest.mark.django_db
def test_teacher_search_by_other_teacher(teacher_client):
    pass


@pytest.mark.django_db
def test_teacher_search_by_student(student_client):
    pass


@pytest.mark.django_db
def test_teacher_search_by_guardian(client: APIClient):
    pass
