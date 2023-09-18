import pytest
from datetime import timedelta
from rest_framework.reverse import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from school_management.tests.factories import ClassRoomFactory

from user_management.models import Student
from user_management.tests.factories import StudentFactory, UserFactory


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
def test_student_create_by_class_teacher_returns_201(teacher_client, generic_user_data):
    client, teacher = teacher_client
    classroom = ClassRoomFactory(teacher=teacher, school=teacher.school)
    data = {
        'user': generic_user_data,
        'classroom_id': classroom.pk,
        'school_id': classroom.school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-list')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Student.objects.count() == 1
    student = Student.objects.first()
    assert student.date_of_birth.strftime('%Y-%m-%d') == data['date_of_birth']
    assert student.user.username == data['user']['username']


@pytest.mark.django_db
@pytest.mark.views
def test_student_create_by_school_admin_returns_201(school_admin_client, generic_user_data):
    client, school_admin = school_admin_client
    school = school_admin.school
    classroom = ClassRoomFactory(school=school)
    data = {
        'user': generic_user_data,
        'classroom_id': classroom.pk,
        'school_id': school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-list')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Student.objects.count() == 1
    student = Student.objects.first()
    assert student.date_of_birth.strftime('%Y-%m-%d') == data['date_of_birth']
    assert student.user.username == data['user']['username']


@pytest.mark.django_db
@pytest.mark.views
def test_student_create_by_superuser_returns_201(superuser_client, generic_user_data):
    client, _ = superuser_client
    classroom = ClassRoomFactory()
    data = {
        'user': generic_user_data,
        'classroom_id': classroom.pk,
        'school_id': classroom.school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-list')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Student.objects.count() == 1
    student = Student.objects.first()
    assert student.date_of_birth.strftime('%Y-%m-%d') == data['date_of_birth']
    assert student.user.username == data['user']['username']


@pytest.mark.django_db
@pytest.mark.views
def test_student_create_adds_revision(superuser_client, generic_user_data):
    client, _ = superuser_client
    classroom = ClassRoomFactory()
    data = {
        'user': generic_user_data,
        'classroom_id': classroom.pk,
        'school_id': classroom.school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-list')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Student.objects.count() == 1
    student = Student.objects.first()
    assert student.versions.count() == 1


#################################### Error path tests #################################

@pytest.mark.django_db
@pytest.mark.views
def test_student_create_without_school_id(superuser_client, generic_user_data):
    client, _ = superuser_client
    classroom = ClassRoomFactory()
    data = {
        'user': generic_user_data,
        'classroom_id': classroom.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-list')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'school_id is required.' in str(response.data)
    assert Student.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.views
def test_student_create_without_classroom_id(superuser_client, generic_user_data):
    client, _ = superuser_client
    classroom = ClassRoomFactory()
    data = {
        'user': generic_user_data,
        'school_id': classroom.school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-list')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'classroom_id is required.' in str(response.data)
    assert Student.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.views
def test_student_create_with_another_student_user(superuser_client):
    client, _ = superuser_client
    classroom = ClassRoomFactory()
    original_student = StudentFactory()
    data = {
        'user_id': original_student.user.pk,
        'classroom_id': classroom.pk,
        'school_id': classroom.school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-list')
    # Try to create another student with the same user
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_409_CONFLICT
    assert f'Student with user_id {original_student.user.pk} already exists.' in str(response.data)
    assert Student.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.views
def test_create_student_without_user_id_returns_400(superuser_client):
    client, _ = superuser_client
    classroom = ClassRoomFactory()
    data = {
        'classroom_id': classroom.pk,
        'school_id': classroom.school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-list')
    # Try to create another student with the same user
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'user or user_id is required.' in str(response.data)
    assert Student.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.views
def test_create_invalid_student_returns_400(superuser_client):
    client, _ = superuser_client
    classroom = ClassRoomFactory()
    user = UserFactory()
    data = {
        'user_id': user.pk,
        'invalid_field': 'invalid_value',
        'classroom_id': classroom.pk,
        'school_id': classroom.school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-list')
    # Try to create another student with the same user
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Unsupported student fields: invalid_field' in str(response.data)
    assert Student.objects.count() == 0


#################################### Permission tests #################################

@pytest.mark.django_db
@pytest.mark.views
def test_create_by_unauthorized_user_returns_403(user_client, generic_data):
    client, _ = user_client
    url = reverse('student-list')
    response = client.post(url, generic_data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Student.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.views
def test_create_by_unauthenticated_user_returns_401(generic_data):
    client = APIClient()
    url = reverse('student-list')
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
    url = reverse('student-list')
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
    url = reverse('student-list')
    response = client.post(url, data, format="json")
    assert school_admin.school != classroom.school
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Student.objects.count() == 0
