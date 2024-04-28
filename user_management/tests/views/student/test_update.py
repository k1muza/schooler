import pytest
from datetime import timedelta
from django.db.models import ForeignKey
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from school_management.tests.factories import ClassFactory, SchoolFactory
from user_management.models import Student
from user_management.tests.factories import StudentFactory


# ######################### Happy path tests #########################


@pytest.mark.views
@pytest.mark.django_db
def test_student_update_by_superuser_returns_200(superuser_client):
    client, _ = superuser_client
    student = StudentFactory()
    updated_data = {
        "id": student.id,
        "school_id": student.school.id,
        "user_id": student.user.id,
        "student_number": "123456",
    }
    url = reverse('student-detail', args=[student.id])
    response = client.put(url, updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    student.refresh_from_db()
    assert student.student_number == updated_data['student_number']


@pytest.mark.views
@pytest.mark.django_db
def test_student_update_by_class_teacher_returns_200(teacher_client):
    client, teacher = teacher_client
    student = StudentFactory(school=teacher.school)
    klass = ClassFactory(teacher=teacher, school=teacher.school)
    klass.students.add(student)
    updated_data = {
        "id": student.id,
        "school_id": student.school.id,
        "user_id": student.user.id,
        "student_number": "123456",
    }
    url = reverse('student-detail', args=[student.id])
    response = client.put(url, updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    student.refresh_from_db()
    assert student.student_number == updated_data['student_number']


@pytest.mark.views
@pytest.mark.django_db
def test_student_update_by_schooladmin_returns_200(administrator_client):
    client, admin = administrator_client
    student = StudentFactory(school=admin.school)
    updated_data = {
        "id": student.id,
        "school_id": student.school.id,
        "user_id": student.user.id,
        "student_number": "123456",
    }
    url = reverse('student-detail', args=[student.id])
    response = client.put(url, updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    student.refresh_from_db()
    assert student.student_number == updated_data['student_number']


@pytest.mark.views
@pytest.mark.django_db
def test_student_update_by_self(student_client):
    client, student = student_client
    updated_data = {
        "id": student.id,
        "school_id": student.school.id,
        "user_id": student.user.id,
        "student_number": "123456",
    }
    url = reverse('student-detail', args=[student.id])
    response = client.put(url, updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    student.refresh_from_db()
    assert student.student_number == updated_data['student_number']

# @pytest.mark.django_db
# @pytest.mark.views
# def test_student_update_by_schooladmin_returns_200(administrator_client):
#     pass


# @pytest.mark.django_db
# @pytest.mark.views
# def test_student_update_by_super_user_returns_200(superuser_client):
#     pass


# @pytest.mark.django_db
# @pytest.mark.views
# def test_student_update_adds_revision(teacher_client):
#     pass


# ######################### Unhappy path tests #########################

# @pytest.mark.django_db
# @pytest.mark.views
# def test_update_with_nonexistent_user_returns_404(teacher_client):
#     pass


# @pytest.mark.django_db
# @pytest.mark.views
# def test_update_with_noneexistent_class_returns_404(teacher_client):
#     pass


# @pytest.mark.django_db
# @pytest.mark.views
# def test_update_with_other_student_user_returns_409(teacher_client):
#     pass


# @pytest.mark.django_db
# @pytest.mark.views
# def test_student_update_by_unrelated_teacher_returns_404(teacher_client):
#     pass


# @pytest.mark.django_db
# @pytest.mark.views
# def test_student_update_by_unrelated_school_admin_returns_404(administrator_client):
#     pass


# @pytest.mark.django_db
# @pytest.mark.views
# def test_update_by_unauthenticated_user_returns_401():
#     pass


# @pytest.mark.django_db
# @pytest.mark.views
# def test_update_with_invalid_foreign_key_returns_400(teacher_client):
#     pass


@pytest.mark.views
@pytest.mark.django_db
def test_student_update_immutable_school_id(superuser_client):
    client, _ = superuser_client
    student = StudentFactory()

    original_school = student.school
    school = SchoolFactory()

    url = reverse("student-detail", args=[student.id])
    updated_data = {
        "id": student.id,
        "school_id": school.id,
        "user_id": student.user.id,
        "student_number": "123456",
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    student.refresh_from_db()
    assert student.school == original_school
