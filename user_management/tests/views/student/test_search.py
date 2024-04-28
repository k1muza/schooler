import pytest
from urllib.parse import urlencode
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from school_management.tests.factories import ClassFactory, SchoolFactory

from user_management.tests.factories import StudentFactory

def setup_students_data(school=None, klass=None):
    if not school:
        school = SchoolFactory()

    if not klass:
        klass = ClassFactory(school=school)

    StudentFactory(user__first_name="John", user__last_name="Doe")
    StudentFactory(user__first_name="John", user__last_name="Doe", school=school)
    StudentFactory(user__first_name="Jane", user__last_name="Doe", school=school)
    StudentFactory(user__first_name="Innocent", user__email="nmy@email.com")

    alice = StudentFactory(user__first_name="Alice", user__username="alice123", school=school)
    bob = StudentFactory(user__first_name="Bob", user__email="bob@email.com", school=school)
    ino = StudentFactory(user__first_name="Innocent", user__email="ino@email.com", school=school)

    klass.students.add(alice, bob, ino)

@pytest.mark.django_db
@pytest.mark.views
def test_student_search_by_school_admin(administrator_client):
    client, schooladmin = administrator_client
    
    setup_students_data(school=schooladmin.school)

    base_url = reverse('student-search')

    # Test search by first_name
    query_string = urlencode({'search': 'John'})
    response = client.get(f'{base_url}?{query_string}')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

    # Test search by last_name
    base_url = reverse('student-search')
    query_string = urlencode({'search': 'Doe'})
    response = client.get(f'{base_url}?{query_string}')
    assert len(response.data) == 2

    # Test search by username
    query_string = urlencode({'search': 'alice123'})
    response = client.get(f'{base_url}?{query_string}')
    assert len(response.data) == 1

    # Test search by email
    query_string = urlencode({'search': 'bob@email.com'})
    response = client.get(f'{base_url}?{query_string}')
    assert len(response.data) == 1

    # Test no matches
    query_string = urlencode({'search': 'no-match'})
    response = client.get(f'{base_url}?{query_string}')
    assert len(response.data) == 0


@pytest.mark.django_db
@pytest.mark.views
def test_student_search_by_other_school_admin(administrator_client):
    client, _ = administrator_client
    setup_students_data()
    base_url = reverse('student-search')
    response = client.get(base_url)
    assert len(response.data) == 0


@pytest.mark.django_db
@pytest.mark.views
def test_student_search_by_teacher(teacher_client):
    client, teacher = teacher_client
    setup_students_data(klass=ClassFactory(teacher=teacher))
    base_url = reverse('student-search')
    query_string = urlencode({'search': 'Alice'})
    response = client.get(f'{base_url}?{query_string}')
    assert len(response.data) == 1

    query_string = urlencode({'search': 'inno'})
    response = client.get(f'{base_url}?{query_string}')
    assert len(response.data) == 1


@pytest.mark.django_db
@pytest.mark.views
def test_student_search_by_unauthenticated_user():
    client = APIClient()
    setup_students_data()
    base_url = reverse('student-search')
    response = client.get(base_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'Authentication credentials were not provided.' in response.data['detail']
