import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user_management.models import Teacher
from user_management.serializers import TeacherSerializer
from user_management.tests.factories import TeacherFactory

@pytest.mark.django_db
def test_teacher_list_by_superuser(superuser_client):
    pass


@pytest.mark.django_db
def test_teacher_list_by_school_admin(administrator_client):
    pass


@pytest.mark.django_db
def test_teacher_list_by_self(teacher_client):
    pass


@pytest.mark.django_db
def test_teacher_list_by_other_teacher(teacher_client):
    pass


@pytest.mark.django_db
def test_teacher_list_by_student(student_client):
    pass


@pytest.mark.django_db
def test_teacher_list_by_guardian(client):
    pass

@pytest.mark.django_db
@pytest.mark.views
def test_get_teacher_list_by_authenticated_user(user_client):
    client, _ = user_client
    TeacherFactory()
    TeacherFactory()

    url = reverse('teacher-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    serializer = TeacherSerializer(Teacher.objects.none(), many=True)
    assert response.data == serializer.data


@pytest.mark.django_db
@pytest.mark.views
def test_get_teacher_list_by_unauthenticated_user():
    client = APIClient()
    url = reverse('teacher-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
