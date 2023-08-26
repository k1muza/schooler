import pytest
from django.urls import reverse
from rest_framework import status
from user_management.models import Teacher

from user_management.tests.factories import TeacherFactory


@pytest.mark.django_db
@pytest.mark.views
def test_delete_teacher(api_client):
    teacher = TeacherFactory()
    url = reverse('teacher-delete', args=[teacher.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == "Teacher deleted successfully"
    assert Teacher.objects.filter(id=teacher.id).count() == 0


@pytest.mark.django_db
@pytest.mark.views
def test_delete_teacher_not_found(api_client):
    url = reverse('teacher-delete', args=[9999])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
