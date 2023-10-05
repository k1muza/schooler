import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user_management.models import Student

from user_management.tests.factories import StudentFactory


######################### Happy path tests #########################

@pytest.mark.django_db
@pytest.mark.views
def test_delete_student_returns_204(superuser_client):
    client, _ = superuser_client
    student = StudentFactory()
    url = reverse('student-detail', args=[student.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Student.objects.filter(id=student.id).count() == 0


@pytest.mark.django_db
@pytest.mark.views
def test_delete_student_not_found(superuser_client):
    client, _ = superuser_client
    url = reverse('student-detail', args=[9999])
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.views
def test_delete_student_by_class_teacher_returns_403(teacher_client):
    client, teacher = teacher_client
    student = StudentFactory(classroom=teacher.classrooms.first())
    url = reverse('student-detail', args=[student.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Student.objects.filter(id=student.id).count() == 1


@pytest.mark.django_db
@pytest.mark.views
def test_delete_student_by_school_admin_returns_204(school_admin_client):
    client, admin = school_admin_client
    student = StudentFactory(school=admin.school)
    url = reverse('student-detail', args=[student.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Student.objects.filter(id=student.id).count() == 0


@pytest.mark.django_db
@pytest.mark.views
def test_delete_student_by_super_user_returns_204(superuser_client):
    client, _ = superuser_client
    student = StudentFactory()
    url = reverse('student-detail', args=[student.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Student.objects.filter(id=student.id).count() == 0


# ######################### Exceptional path tests #########################

@pytest.mark.django_db
@pytest.mark.views
def test_delete_student_by_student_returns_403(student_client):
    client, student = student_client
    url = reverse('student-detail', args=[student.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Student.objects.filter(id=student.id).count() == 1


@pytest.mark.django_db
@pytest.mark.views
def test_delete_student_by_guardian_returns_403(guardian_client):
    client, guardian = guardian_client
    student = StudentFactory(guardians=[guardian])
    url = reverse('student-detail', args=[student.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Student.objects.filter(id=student.id).count() == 1


@pytest.mark.django_db
@pytest.mark.views
def test_delete_student_by_other_class_teacher_returns_404(teacher_client):
    client, _ = teacher_client
    student = StudentFactory()
    url = reverse('student-detail', args=[student.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Student.objects.filter(id=student.id).count() == 1


@pytest.mark.django_db
@pytest.mark.views
def test_delete_student_by_other_school_admin_returns_404(school_admin_client):
    client, _ = school_admin_client
    student = StudentFactory()
    url = reverse('student-detail', args=[student.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Student.objects.filter(id=student.id).count() == 1


@pytest.mark.django_db
@pytest.mark.views
def test_delete_student_by_other_user_returns_403(user_client):
    client, _ = user_client
    student = StudentFactory()
    url = reverse('student-detail', args=[student.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Student.objects.filter(id=student.id).count() == 1


@pytest.mark.django_db
@pytest.mark.views
def test_delete_student_by_unauthenticated_returns_401():
    client = APIClient()
    student = StudentFactory()
    url = reverse('student-detail', args=[student.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Student.objects.filter(id=student.id).count() == 1
