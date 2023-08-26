import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user_management.models import Teacher
from user_management.serializers import TeacherSerializer
from user_management.tests.factories import TeacherFactory


@pytest.mark.django_db
@pytest.mark.views
def test_get_teacher_list_authenticated(api_client):
    teacher1 = TeacherFactory()
    teacher2 = TeacherFactory()

    url = reverse('teacher-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    assert response.data == serializer.data


@pytest.mark.django_db
@pytest.mark.views
def test_get_teacher_list_unauthenticated():
    client = APIClient()
    url = reverse('teacher-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
