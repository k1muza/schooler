import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from school_management.tests.factories import ClassFactory
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
def test_delete_student_by_school_admin_returns_204(schooladmin_client):
    client, admin = schooladmin_client
    student = StudentFactory(school=admin.school)
    url = reverse('student-detail', args=[student.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Student.objects.filter(id=student.id).count() == 0


######################### Perm tests #########################

@pytest.mark.parametrize("client_fixture, expected_status", [
    ('schooladmin_client', status.HTTP_404_NOT_FOUND),
    ('teacher_client', status.HTTP_404_NOT_FOUND),
    ('student_client', status.HTTP_404_NOT_FOUND),
    ('guardian_client', status.HTTP_404_NOT_FOUND),
    ('user_client', status.HTTP_404_NOT_FOUND),
])
@pytest.mark.django_db
@pytest.mark.views
def test_delete_by_other_admin(request, client_fixture, expected_status):
    client, _ = request.getfixturevalue(client_fixture)
    student = StudentFactory()
    url = reverse('student-detail', args=[student.id])
    response = client.delete(url)
    assert response.status_code == expected_status
    assert Student.objects.filter(id=student.id).count() == 1


@pytest.mark.django_db
@pytest.mark.views
def test_delete_student_by_class_teacher_returns_403(teacher_client):
    client, teacher = teacher_client
    student = StudentFactory(school=teacher.school)
    klass = ClassFactory(teacher=teacher, school=teacher.school)
    klass.students.add(student)
    url = reverse('student-detail', args=[student.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Student.objects.filter(id=student.id).count() == 1


########################### Exceptional path tests #########################

@pytest.mark.django_db
@pytest.mark.views
def test_delete_student_by_self(student_client):
    client, student = student_client
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


@pytest.mark.django_db
@pytest.mark.views
def test_delete_student_not_found(superuser_client):
    client, _ = superuser_client
    url = reverse('student-detail', args=[9999])
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
