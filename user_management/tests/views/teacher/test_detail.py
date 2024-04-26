import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user_management.tests.factories import TeacherFactory


@pytest.mark.django_db
@pytest.mark.views
def test_get_teacher_detail_authenticated_not_found(user_client):
    client, _ = user_client
    teacher = TeacherFactory()
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.views
def test_get_teacher_detail_unauthenticated_not_found():
    teacher = TeacherFactory()
    client = APIClient()
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.views
def test_get_teacher_detail_not_found(user_client):
    client, _ = user_client
    url = reverse('teacher-detail', args=[999])
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
