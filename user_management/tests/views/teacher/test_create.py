import pytest
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from school_management.tests.factories import ClassRoomFactory, SchoolFactory
from user_management.models import Teacher


@pytest.mark.django_db
def test_teacher_create_success(api_client):
    school = SchoolFactory()
    user_data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@email.com',
        'first_name': 'Test',
        'last_name': 'User',
    }
    data = {
        'user': user_data,
        'school_id': school.pk,
        'qualifications': 'Ph.D. in Education',
    }
    url = reverse('teacher-create')
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Teacher.objects.count() == 1
    teacher = Teacher.objects.first()
    assert teacher.qualifications == data['qualifications']
    assert teacher.user.username == user_data['username']


@pytest.mark.django_db
def test_teacher_create_unauthenticated():
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
        'qualifications': 'Ph.D. in Education',
    }
    url = reverse('teacher-create')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Teacher.objects.count() == 0

@pytest.mark.django_db
@pytest.mark.views
def test_teacher_create_validation_error(api_client):
    data = {
        'qualifications': 'Ph.D. in Education',
    }
    url = reverse('teacher-create')
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'school_id is required' in str(response.data)

@pytest.mark.django_db
@pytest.mark.views
def test_teacher_create_unauthenticated():
    client = APIClient()
    data = {
        'user': {
            'username': 'testuser',
            'password': 'testpass',
            'email': 'test@email.com',
            'first_name': 'Test',
            'last_name': 'User',
        },
        'qualifications': 'Ph.D. in Education',
    }
    url = reverse('teacher-create')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
