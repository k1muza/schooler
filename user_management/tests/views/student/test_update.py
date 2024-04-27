import pytest
from datetime import timedelta
from django.db.models import ForeignKey
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from school_management.tests.factories import ClassFactory
from user_management.models import Student
from user_management.tests.factories import StudentFactory


# ######################### Happy path tests #########################

@pytest.mark.django_db
@pytest.mark.views
def test_student_update_by_class_teacher_returns_200(teacher_client):
    client, teacher = teacher_client
    student = StudentFactory(school=teacher.school)
    klass = ClassFactory(teacher=teacher, school=teacher.school)
    klass.students.add(student)
    updated_data = {
        "id": student.id,
        "school_id": student.school.id,
        "user_id": student.user.id,
        "date_of_birth": (timezone.now() - timedelta(weeks=52*7)).strftime('%Y-%m-%d'),
        "student_number": "123456",
    }
    url = reverse('student-detail', args=[student.id])
    response = client.put(url, updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    student.refresh_from_db()
    assert student.date_of_birth.strftime('%Y-%m-%d') == updated_data['date_of_birth']
    assert student.student_number == updated_data['student_number']


# @pytest.mark.django_db
# @pytest.mark.views
# def test_student_update_by_schooladmin_returns_200(schooladmin_client):
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
# def test_student_update_by_unrelated_school_admin_returns_404(schooladmin_client):
#     pass


# @pytest.mark.django_db
# @pytest.mark.views
# def test_update_by_unauthenticated_user_returns_401():
#     pass


# @pytest.mark.django_db
# @pytest.mark.views
# def test_update_with_invalid_foreign_key_returns_400(teacher_client):
#     pass

