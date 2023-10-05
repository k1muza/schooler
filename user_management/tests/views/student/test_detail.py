import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user_management.tests.factories import StudentFactory


######################### Happy path tests #########################


@pytest.mark.django_db
@pytest.mark.views
def test_get_by_class_teacher_returns_200(teacher_client):
    client, teacher = teacher_client
    student = StudentFactory(classroom=teacher.classrooms.first())
    url = reverse('student-detail', args=[student.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.views
def test_get_by_school_admin_returns_200(school_admin_client):
    client, admin = school_admin_client
    student = StudentFactory(school=admin.school)
    url = reverse('student-detail', args=[student.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.views
def test_get_by_student_returns_200(student_client):
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
def test_get_student_detail_by_super_user(superuser_client):
    client, _ = superuser_client
    student = StudentFactory()
    url = reverse('student-detail', args=[student.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

######################### Exceptional path tests #########################

@pytest.mark.django_db
@pytest.mark.views
def test_get_student_detail_unauthenticated_401():
    student = StudentFactory()
    client = APIClient()
    url = reverse('student-detail', args=[student.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.views
def test_get_student_detail_by_other_class_teacher_404(teacher_client):
    client, _ = teacher_client
    student = StudentFactory()
    url = reverse('student-detail', args=[student.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.views
def test_get_student_detail_by_other_school_admin_404(school_admin_client):
    client, _ = school_admin_client
    student = StudentFactory()
    url = reverse('student-detail', args=[student.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.views
def test_get_student_detail_by_other_student_404(student_client):
    client, _ = student_client
    student = StudentFactory()
    url = reverse('student-detail', args=[student.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.views
def test_get_student_detail_by_other_guardian_404(guardian_client):
    client, _ = guardian_client
    student = StudentFactory()
    url = reverse('student-detail', args=[student.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.views
def test_get_student_detail_by_other_user_403(user_client):
    client, _ = user_client
    student = StudentFactory()
    url = reverse('student-detail', args=[student.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
