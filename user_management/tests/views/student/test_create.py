import pytest
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from school_management.tests.factories import ClassRoomFactory, SchoolFactory

from user_management.models import Student


@pytest.mark.django_db
@pytest.mark.views
def test_student_create_success(api_client):
    school = SchoolFactory()
    user_data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@email.com',
        'first_name': 'Test',
        'last_name': 'User',
    }
    classroom_data = {
        'name': 'Classroom 1',
        'school_id': school.pk
    }
    data = {
        'user': user_data,
        'classroom': classroom_data,
        'school_id': school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-create')
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Student.objects.count() == 1
    student = Student.objects.first()
    assert student.date_of_birth == data['date_of_birth']
    assert student.user.username == user_data['username']


@pytest.mark.django_db
@pytest.mark.views
def test_student_create_success():
    client = APIClient()
    classroom = ClassRoomFactory()
    user_data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@email.com',
        'first_name': 'Test',
        'last_name': 'User',
    }
    data = {
        'user': user_data,
        'classroom_id': classroom.pk,
        'school_id': classroom.school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-create')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Student.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.views
def test_student_create_missing_school_id(api_client):
    classroom = ClassRoomFactory()
    user_data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@email.com',
        'first_name': 'Test',
        'last_name': 'User',
    }
    data = {
        'user': user_data,
        'classroom_id': classroom.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-create')
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'school_id is required.' in str(response.data)


@pytest.mark.django_db
@pytest.mark.views
def test_student_create_missing_classroom_id(api_client):
    classroom = ClassRoomFactory()
    user_data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@email.com',
        'first_name': 'Test',
        'last_name': 'User',
    }
    data = {
        'user': user_data,
        'school_id': classroom.school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-create')
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'classroom_id is required.' in str(response.data)


@pytest.mark.django_db
@pytest.mark.views
def test_student_create_unauthenticated():
    client = APIClient()
    data = {
        'user': {
            'username': 'testuser',
            'password': 'testpass',
            'email': 'test@email.com',
            'first_name': 'Test',
            'last_name': 'User',
        },
    }
    url = reverse('student-create')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
