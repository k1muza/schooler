import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from school_management.tests.factories import ClassFactory
from user_management.tests.factories import StudentFactory


######################### Happy path tests #########################


@pytest.mark.django_db
@pytest.mark.views
def test_get_student_by_class_teacher(teacher_client):
    client, teacher = teacher_client
    student = StudentFactory(school=teacher.school)
    klass = ClassFactory(teacher=teacher)
    klass.students.add(student)
    url = reverse('student-detail', args=[student.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.views
def test_get_student_by_schooladmin(schooladmin_client):
    client, admin = schooladmin_client
    student = StudentFactory(school=admin.school)
    url = reverse('student-detail', args=[student.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.views
def test_get_student_by_self(student_client):
    client, student = student_client
    url = reverse('student-detail', args=[student.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.views
def test_get_by_guardian_returns_200(guardian_client):
    client, guardian = guardian_client
    student = guardian.students.first()
    url = reverse('student-detail', args=[student.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.views
def test_get_student_by_super_user(superuser_client):
    client, _ = superuser_client
    student = StudentFactory()
    url = reverse('student-detail', args=[student.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("client_fixture, expected_status", [
    ('schooladmin_client', status.HTTP_404_NOT_FOUND),
    ('teacher_client', status.HTTP_404_NOT_FOUND),
    ('student_client', status.HTTP_404_NOT_FOUND),
    ('guardian_client', status.HTTP_404_NOT_FOUND),
    ('user_client', status.HTTP_404_NOT_FOUND),
])
@pytest.mark.django_db
@pytest.mark.views
def test_get_student_by_other_class_teacher_404(request, client_fixture, expected_status):
    client, _ = request.getfixturevalue(client_fixture)
    student = StudentFactory()
    url = reverse('student-detail', args=[student.id])
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.views
def test_get_student_unauthenticated_401():
    student = StudentFactory()
    client = APIClient()
    url = reverse('student-detail', args=[student.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
