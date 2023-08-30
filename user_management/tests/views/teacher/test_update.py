import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from user_management.tests.factories import TeacherFactory


@pytest.mark.django_db
@pytest.mark.views
def test_teacher_update_authenticated(user_client):
    client, _ = user_client
    teacher = TeacherFactory()

    url = reverse("teacher-update", args=[teacher.id])
    updated_data = {
        "school_id": teacher.school.id,
        "qualifications": "Updated qualifications",
        "user_id": teacher.user.id,
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    teacher.refresh_from_db()
    assert teacher.qualifications == updated_data["qualifications"]


@pytest.mark.django_db
@pytest.mark.views
def test_teacher_update_unauthenticated():
    teacher = TeacherFactory()
    client = APIClient()
    url = reverse("teacher-update", args=[teacher.id])
    response = client.put(url, {}, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.views
def test_teacher_update_not_found(user_client):
    client, _ = user_client
    url = reverse("teacher-update", args=[999])
    response = client.put(url, {}, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND
