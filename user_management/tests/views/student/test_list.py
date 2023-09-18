import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user_management.serializers import StudentSerializer
from user_management.tests.factories import StudentFactory

######################### Happy path tests #########################

@pytest.mark.django_db
@pytest.mark.views
def test_get_list_by_teacher_200(teacher_client):
    client, teacher = teacher_client
    StudentFactory.create_batch(2)
    students = StudentFactory.create_batch(3, classroom=teacher.classrooms.first())
    url = reverse('student-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == StudentSerializer(students, many=True).data
    assert len(response.data) == 3

@pytest.mark.django_db
@pytest.mark.views
def test_get_list_by_school_admin_200(school_admin_client):
    client, admin = school_admin_client
    StudentFactory.create_batch(2)
    students = StudentFactory.create_batch(3, school=admin.school)
    url = reverse('student-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == StudentSerializer(students, many=True).data
    assert len(response.data) == 3

@pytest.mark.django_db
@pytest.mark.views
def test_get_list_by_student_200(student_client):
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
    students = guardian.students.all()
    url = reverse('student-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == StudentSerializer(students, many=True).data
    assert len(response.data) == 3

@pytest.mark.django_db
@pytest.mark.views
def test_get_list_by_super_user_200(superuser_client):
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
