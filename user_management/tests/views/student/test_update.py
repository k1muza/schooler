import pytest
from datetime import timedelta
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from user_management.models import Student
from user_management.tests.factories import StudentFactory


@pytest.mark.django_db
@pytest.mark.views
def test_student_update_authenticated(user_client):
    client, _ = user_client
    student: Student = StudentFactory()

    url = reverse("student-update", args=[student.id])
    updated_data = {
        "school_id": student.school.pk,
        "date_of_birth": (timezone.now() - timedelta(weeks=52*8)).strftime("%Y-%m-%d"),
        "user_id": student.user.pk,
        "classroom_id": student.classroom.pk
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    student.refresh_from_db()
    assert student.date_of_birth.strftime("%Y-%m-%d") == updated_data["date_of_birth"]


@pytest.mark.django_db
@pytest.mark.views
def test_student_update_unauthenticated():
    student = StudentFactory()
    client = APIClient()
    url = reverse("student-update", args=[student.id])
    response = client.put(url, {}, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.views
def test_student_update_not_found(user_client):
    client, _ = user_client
    url = reverse("student-update", args=[999])
    response = client.put(url, {}, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND
