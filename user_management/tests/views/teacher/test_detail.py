import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from school_management.tests.factories import ClassFactory, SchoolFactory
from user_management.tests.factories import GuardianshipFactory, StudentFactory, TeacherFactory, UserFactory
from school_management.models import Class


######################### Happy path tests #########################

@pytest.mark.parametrize("client_fixture, expected_status", [
    ('superuser_client', status.HTTP_200_OK),
    ('administrator_client', status.HTTP_200_OK),
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
def test_get_teacher_by_class_student_guardian(client):
    student = StudentFactory()
    guardian = GuardianshipFactory(user=student.user, guardian=UserFactory())
    teacher = TeacherFactory()
    klass: Class = ClassFactory(teacher=teacher)
    klass.students.add(student)
    client.force_login(guardian.guardian)
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

######################### Perm tests #########################

@pytest.mark.parametrize("client_fixture, expected_status", [
    ('administrator_client', status.HTTP_404_NOT_FOUND),
    ('teacher_client', status.HTTP_404_NOT_FOUND),
    ('student_client', status.HTTP_404_NOT_FOUND),
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


@pytest.mark.views
@pytest.mark.django_db
def test_get_teacher_by_guardian_of_other_student(client):
    guardian = GuardianshipFactory()
    teacher = TeacherFactory()
    klass = ClassFactory(teacher=teacher)
    klass.students.add(StudentFactory())
    client.force_login(guardian.guardian)
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


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
