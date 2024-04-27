import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from school_management.tests.factories import ClassFactory
from user_management.serializers import StudentSerializer
from user_management.tests.factories import StudentFactory

######################### Happy path tests #########################

@pytest.mark.django_db
@pytest.mark.views
def test_get_list_by_teacher_200(teacher_client):
    client, teacher = teacher_client
    StudentFactory.create_batch(2)
    students = StudentFactory.create_batch(3)
    klass = ClassFactory(teacher=teacher, school=teacher.school)
    klass.students.add(*students)
    url = reverse('student-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == StudentSerializer(students, many=True).data
    assert len(response.data) == 3


@pytest.mark.django_db
@pytest.mark.views
def test_get_list_by_school_admin_200(schooladmin_client):
    client, admin = schooladmin_client
    StudentFactory.create_batch(2)
    students = StudentFactory.create_batch(3, school=admin.school)
    url = reverse('student-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == StudentSerializer(students, many=True).data
    assert len(response.data) == 3


@pytest.mark.django_db
@pytest.mark.views
def test_get_list_by_self(student_client):
    client, student = student_client
    StudentFactory.create_batch(2)
    url = reverse('student-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == StudentSerializer([student], many=True).data
    assert len(response.data) == 1


@pytest.mark.django_db
@pytest.mark.views
def test_get_list_by_guardian_200(guardian_client):
    client, guardian = guardian_client
    StudentFactory.create_batch(2)
    url = reverse('student-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == StudentSerializer(guardian.students.all(), many=True).data
    assert len(response.data) == guardian.students.count()


@pytest.mark.django_db
@pytest.mark.views
def test_get_list_by_superuser_200(superuser_client):
    client, _ = superuser_client
    students = StudentFactory.create_batch(5)
    url = reverse('student-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == StudentSerializer(students, many=True).data
    assert len(response.data) == 5


######################### Exceptional path tests #########################

@pytest.mark.django_db
@pytest.mark.views
def test_get_list_unauthenticated_401():
    StudentFactory.create_batch(5)
    url = reverse('student-list')
    client = APIClient()
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data == {'detail': 'Authentication credentials were not provided.'}
