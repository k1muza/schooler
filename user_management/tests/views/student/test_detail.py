import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user_management.serializers import StudentSerializer
from user_management.tests.factories import StudentFactory


@pytest.mark.django_db
@pytest.mark.views
def test_get_student_detail_authenticated(api_client):
    student = StudentFactory()
    url = reverse('student-detail', args=[student.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    serializer = StudentSerializer(student)
    assert response.data == serializer.data


@pytest.mark.django_db
@pytest.mark.views
def test_get_student_detail_unauthenticated():
    student = StudentFactory()
    client = APIClient()
    url = reverse('student-detail', args=[student.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.views
def test_get_student_detail_not_found(api_client):
    url = reverse('student-detail', args=[999])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
