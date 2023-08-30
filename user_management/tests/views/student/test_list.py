import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user_management.models import Student
from user_management.serializers import StudentSerializer
from user_management.tests.factories import StudentFactory

@pytest.mark.django_db
@pytest.mark.views
def test_get_student_list_authenticated(user_client):
    client, _ = user_client
    student1 = StudentFactory()
    student2 = StudentFactory()

    url = reverse('student-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    assert response.data == serializer.data


@pytest.mark.django_db
@pytest.mark.views
def test_get_student_list_unauthenticated():
    client = APIClient()
    url = reverse('student-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
