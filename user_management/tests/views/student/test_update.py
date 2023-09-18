import pytest
from datetime import timedelta
from django.db.models import ForeignKey
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from user_management.models import Student
from user_management.tests.factories import StudentFactory


######################### Happy path tests #########################

@pytest.mark.django_db
@pytest.mark.views
def test_student_update_by_class_teacher_returns_200(teacher_client):
    client, teacher = teacher_client
    student: Student = StudentFactory(classroom__teacher=teacher)
    url = reverse("student-detail", args=[student.id])
    updated_data = {
        "id": student.pk,
        "date_of_birth": (timezone.now() - timedelta(weeks=52*8)).strftime("%Y-%m-%d"),
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    student.refresh_from_db()
    assert student.date_of_birth.strftime("%Y-%m-%d") == updated_data["date_of_birth"]

@pytest.mark.django_db
@pytest.mark.views
def test_student_update_by_schooladmin_returns_200(school_admin_client):
    client, school_admin = school_admin_client
    student: Student = StudentFactory(school=school_admin.school)
    url = reverse("student-detail", args=[student.id])
    updated_data = {
        "id": student.pk,
        "date_of_birth": (timezone.now() - timedelta(weeks=52*8)).strftime("%Y-%m-%d"),
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    student.refresh_from_db()
    assert student.date_of_birth.strftime("%Y-%m-%d") == updated_data["date_of_birth"]

@pytest.mark.django_db
@pytest.mark.views
def test_student_update_by_super_user_returns_200(superuser_client):
    client, _ = superuser_client
    student: Student = StudentFactory()
    url = reverse("student-detail", args=[student.id])
    updated_data = {
        "id": student.pk,
        "date_of_birth": (timezone.now() - timedelta(weeks=52*8)).strftime("%Y-%m-%d"),
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    student.refresh_from_db()
    assert student.date_of_birth.strftime("%Y-%m-%d") == updated_data["date_of_birth"]


@pytest.mark.django_db
@pytest.mark.views
def test_student_update_adds_revision(teacher_client):
    client, teacher = teacher_client
    student: Student = StudentFactory(classroom__teacher=teacher)
    url = reverse("student-detail", args=[student.id])
    updated_data = {
        "id": student.pk,
        "date_of_birth": (timezone.now() - timedelta(weeks=52*8)).strftime("%Y-%m-%d"),
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    student.refresh_from_db()
    assert student.versions.count() == 2


######################### Unhappy path tests #########################

@pytest.mark.django_db
@pytest.mark.views
def test_update_with_nonexistent_user_returns_404(teacher_client):
    client, teacher = teacher_client
    student: Student = StudentFactory(classroom__teacher=teacher)
    url = reverse("student-detail", args=[student.id])
    updated_data = {
        "id": student.pk,
        "user_id": 999
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    student.refresh_from_db()
    assert student.user.pk != updated_data["user_id"]


@pytest.mark.django_db
@pytest.mark.views
def test_update_with_noneexistent_classroom_returns_404(teacher_client):
    client, teacher = teacher_client
    student: Student = StudentFactory(classroom__teacher=teacher)
    url = reverse("student-detail", args=[999])
    updated_data = {
        "id": student.id,
        "classroom_id": 999
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.views
def test_update_with_other_student_user_returns_409(teacher_client):
    client, teacher = teacher_client
    student: Student = StudentFactory(classroom__teacher=teacher)
    url = reverse("student-detail", args=[student.id])
    other_student: Student = StudentFactory(classroom__teacher=teacher)
    updated_data = {
        "id": student.pk,
        "user_id": other_student.user.pk,
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_409_CONFLICT
    student.refresh_from_db()
    assert student.user.pk != updated_data["user_id"]


@pytest.mark.django_db
@pytest.mark.views
def test_student_update_by_unrelated_teacher_returns_403(teacher_client):
    client, teacher = teacher_client
    student: Student = StudentFactory()
    url = reverse("student-detail", args=[student.id])
    updated_data = {
        "id": student.pk,
        "date_of_birth": (timezone.now() - timedelta(weeks=52*8)).strftime("%Y-%m-%d"),
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    student.refresh_from_db()
    assert student.date_of_birth.strftime("%Y-%m-%d") != updated_data["date_of_birth"]


@pytest.mark.django_db
@pytest.mark.views
def test_student_update_by_unrelated_school_admin_returns_403(school_admin_client):
    client, school_admin = school_admin_client
    student: Student = StudentFactory()
    url = reverse("student-detail", args=[student.id])
    updated_data = {
        "id": student.pk,
        "date_of_birth": (timezone.now() - timedelta(weeks=52*8)).strftime("%Y-%m-%d"),
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    student.refresh_from_db()
    assert student.date_of_birth.strftime("%Y-%m-%d") != updated_data["date_of_birth"]


@pytest.mark.django_db
@pytest.mark.views
def test_update_by_unauthenticated_user_returns_401():
    student: Student = StudentFactory()
    client = APIClient()
    url = reverse("student-detail", args=[student.id])
    updated_data = {
        "id": student.pk,
        "date_of_birth": (timezone.now() - timedelta(weeks=52*8)).strftime("%Y-%m-%d"),
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    student.refresh_from_db()
    assert student.date_of_birth.strftime("%Y-%m-%d") != updated_data["date_of_birth"]

@pytest.mark.django_db
@pytest.mark.views
def test_update_with_invalid_foreign_key_returns_400(teacher_client):
    client, teacher = teacher_client
    student: Student = StudentFactory(classroom__teacher=teacher)
    url = reverse("student-detail", args=[student.id])

    # Loop through each field in the Student model
    for field in Student._meta.get_fields():
        # Check if the field is a ForeignKey
        if isinstance(field, ForeignKey):
            # Get the name of the ForeignKey field and construct an invalid update payload
            field_name = f"{field.name}_id"
            updated_data = {
                "id": student.pk,
                field_name: 999  # Invalid ID
            }

            # Make the API request
            response = client.put(url, updated_data, format="json")

            # Check if the status code is 400 Bad Request
            assert response.status_code == status.HTTP_404_NOT_FOUND

            # Refresh the student object from the database
            student.refresh_from_db()

            # Check if the ForeignKey field has not been updated
            assert getattr(student, field_name) != updated_data[field_name]

