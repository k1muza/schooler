import pytest
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from school_management.tests.factories import ClassRoomFactory

from user_management.models import Student


@pytest.fixture
def generic_user_data():
    return {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@email.com',
        'first_name': 'Test',
        'last_name': 'User',
    }

@pytest.fixture
def generic_data(generic_user_data):
    classroom = ClassRoomFactory()
    return {
        'user': generic_user_data,
        'classroom_id': classroom.pk,
        'school_id': classroom.school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }

######################### Happy path tests #########################

@pytest.mark.django_db
@pytest.mark.views
def test_student_create_by_class_teacher_returns_401(teacher_client, generic_user_data):
    client, teacher = teacher_client
    classroom = ClassRoomFactory(teacher=teacher, school=teacher.school)
    data = {
        'user': generic_user_data,
        'classroom_id': classroom.pk,
        'school_id': classroom.school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-create')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Student.objects.count() == 1
    student = Student.objects.first()
    assert student.date_of_birth.strftime('%Y-%m-%d') == data['date_of_birth']
    assert student.user.username == data['user']['username']



@pytest.mark.django_db
@pytest.mark.views
def test_student_create_by_school_admin_returns_401(school_admin_client, generic_user_data):
    client, school_admin = school_admin_client
    school = school_admin.school
    classroom = ClassRoomFactory(school=school)
    data = {
        'user': generic_user_data,
        'classroom_id': classroom.pk,
        'school_id': school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-create')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Student.objects.count() == 1
    student = Student.objects.first()
    assert student.date_of_birth.strftime('%Y-%m-%d') == data['date_of_birth']
    assert student.user.username == data['user']['username']


#################################### Error path tests #################################

@pytest.mark.django_db
@pytest.mark.views
def test_student_create_missing_school_id(user_client, generic_user_data):
    client, _ = user_client
    classroom = ClassRoomFactory()
    data = {
        'user': generic_user_data,
        'classroom_id': classroom.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-create')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'school_id is required.' in str(response.data)


@pytest.mark.django_db
@pytest.mark.views
def test_student_create_missing_classroom_id(user_client, generic_user_data):
    client, _ = user_client
    classroom = ClassRoomFactory()
    data = {
        'user': generic_user_data,
        'school_id': classroom.school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-create')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'classroom_id is required.' in str(response.data)


#################################### Permission tests #################################

@pytest.mark.django_db
@pytest.mark.views
def test_create_by_unauthorized_user_returns_403(user_client, generic_data):
    client, _ = user_client
    url = reverse('student-create')
    response = client.post(url, generic_data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Student.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.views
def test_create_by_unauthenticated_user_returns_401(generic_data):
    client = APIClient()
    url = reverse('student-create')
    response = client.post(url, generic_data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.views
def test_student_create_by_unrelated_teacher_returns_403(teacher_client, generic_user_data):
    client, teacher = teacher_client
    classroom = ClassRoomFactory(school=teacher.school) # teacher is not assigned to this classroom
    data = {
        'user': generic_user_data,
        'classroom_id': classroom.pk,
        'school_id': classroom.school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-create')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Student.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.views
def test_student_create_by_unrelated_school_admin_returns_403(school_admin_client, generic_user_data):
    client, school_admin = school_admin_client
    classroom = ClassRoomFactory() # teacher is not assigned to this classroom
    data = {
        'user': generic_user_data,
        'classroom_id': classroom.pk,
        'school_id': classroom.school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-create')
    response = client.post(url, data, format="json")
    assert school_admin.school != classroom.school
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Student.objects.count() == 0
