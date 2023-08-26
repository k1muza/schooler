import pytest
from django.urls import reverse
from rest_framework import status
from user_management.models import Student

from user_management.tests.factories import StudentFactory


@pytest.mark.django_db
@pytest.mark.views
def test_delete_student(api_client):
    student = StudentFactory()
    url = reverse('student-delete', args=[student.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == "Student deleted successfully"
    assert Student.objects.filter(id=student.id).count() == 0


@pytest.mark.django_db
@pytest.mark.views
def test_delete_student_not_found(api_client):
    url = reverse('student-delete', args=[9999])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
