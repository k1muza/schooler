import pytest
from datetime import timedelta
from rest_framework.reverse import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from school_management.tests.factories import ClassFactory, SchoolFactory

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
    klass = ClassFactory()
    return {
        'user': generic_user_data,
        'school_id': klass.school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }

######################### Happy path tests #########################

@pytest.mark.django_db
@pytest.mark.views
def test_student_create_by_class_teacher(teacher_client, generic_user_data):
    client, teacher = teacher_client
    klass = ClassFactory(teacher=teacher, school=teacher.school)
    data = {
        'user': generic_user_data,
        'school_id': klass.school.pk,
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
def test_student_create_by_school_admin(schooladmin_client, generic_user_data):
    client, school_admin = schooladmin_client
    school = school_admin.school
    data = {
        'user': generic_user_data,
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
def test_student_create_by_superuser(superuser_client, generic_user_data):
    client, _ = superuser_client
    school = SchoolFactory()
    data = {
        'user': generic_user_data,
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
def test_student_create_adds_revision(superuser_client, generic_user_data):
    client, _ = superuser_client
    klass = ClassFactory()
    data = {
        'user': generic_user_data,
        'school_id': klass.school.pk,
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
    data = {
        'user': generic_user_data,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-list')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'No school_id specified.' in str(response.data)
    assert Student.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.views
def test_student_create_with_invalid_school_id(superuser_client, generic_user_data):
    client, _ = superuser_client
    data = {
        'user': generic_user_data,
        'school_id': 9999999,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-list')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert 'School with id 9999999 does not exist.' in str(response.data)
    assert Student.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.views
def test_student_create_with_another_student_user(superuser_client):
    client, _ = superuser_client
    school = SchoolFactory()
    original_student = StudentFactory()
    data = {
        'user_id': original_student.user.pk,
        'school_id': school.pk,
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
    school = SchoolFactory()
    data = {
        'school_id': school.pk,
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
    school = SchoolFactory()
    user = UserFactory()
    data = {
        'user_id': user.pk,
        'invalid_field': 'invalid_value',
        'school_id': school.pk,
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
def test_student_create_by_teacher_from_different_school(teacher_client, generic_user_data):
    client, _ = teacher_client
    data = {
        'user': generic_user_data,
        'school_id': SchoolFactory().pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-list')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Student.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.views
def test_student_create_by_unrelated_school_admin_returns_403(schooladmin_client, generic_user_data):
    client, school_admin = schooladmin_client
    school = SchoolFactory()
    data = {
        'user': generic_user_data,
        'school_id': school.pk,
        'date_of_birth': (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
    }
    url = reverse('student-list')
    response = client.post(url, data, format="json")
    assert school_admin.school != school
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Student.objects.count() == 0
