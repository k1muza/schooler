import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from school_management.tests.factories import ClassFactory, SchoolFactory
from user_management.tests.factories import StudentFactory, TeacherFactory
from school_management.models import Class


######################### Happy path tests #########################

@pytest.mark.parametrize("client_fixture, expected_status", [
    ('superuser_client', status.HTTP_200_OK),
    ('schooladmin_client', status.HTTP_200_OK),
])
@pytest.mark.django_db
@pytest.mark.views
def test_get_teacher_by_admins(client_fixture, expected_status, request):
    client, admin = request.getfixturevalue(client_fixture)
    kwargs = {
        'school': admin.school if hasattr(admin, 'school') else SchoolFactory()
    }
    teacher = TeacherFactory(**kwargs)
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.views
def test_get_teacher_by_self(teacher_client):
    client, teacher = teacher_client
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.views
def test_get_teacher_by_class_student(student_client):
    client, student = student_client
    teacher = TeacherFactory()
    klass = ClassFactory(teacher=teacher)
    klass.students.add(student)
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.views
def test_get_teacher_by_class_student_guardian(guardian_client):
    student = StudentFactory()
    teacher = TeacherFactory()
    klass: Class = ClassFactory(teacher=teacher)
    klass.students.add(student)
    client, guardian = guardian_client
    guardian.students.add(student)
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

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
def test_get_teacher_by_unpriv_admin(client_fixture, expected_status, request):
    client, _ = request.getfixturevalue(client_fixture)
    teacher = TeacherFactory()
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.views
def test_get_teacher_by_unauthenticated_user():
    teacher = TeacherFactory()
    client = APIClient()
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


####################### Edge cases #######################

@pytest.mark.django_db
@pytest.mark.views
def test_get_teacher_not_found(superuser_client):
    client, _ = superuser_client
    TeacherFactory()
    url = reverse('teacher-detail', args=[999])
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
