import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from reversion.models import Version

from user_management.models import Teacher
from user_management.tests.factories import TeacherFactory


######################### Happy path tests #########################
@pytest.mark.django_db
@pytest.mark.views
def test_delete_teacher_by_school_admin(school_admin_client):
    client, schooladmin = school_admin_client
    teacher = TeacherFactory(school=schooladmin.school)
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Teacher.objects.filter(id=teacher.id).count() == 0


@pytest.mark.django_db
def test_delete_teacher_creates_version(school_admin_client):
    client, schooladmin = school_admin_client
    # Setup: Create a Teacher instance to test deletion
    teacher = TeacherFactory(school=schooladmin.school)
    
    # Ensure the teacher exists
    assert Teacher.objects.filter(user=teacher.user).exists()

    url = reverse('teacher-detail', args=[teacher.id])
    response = client.delete(url)
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Teacher.objects.filter(id=teacher.id).count() == 0
    
    # Test: Check if a version for the deleted teacher exists
    versions = Version.objects.get_for_object_reference(Teacher, teacher.id)
    assert versions.exists(), "No version found for the deleted teacher"
    
    # Assert the user if needed
    last_version = versions.first()
    assert last_version.revision.user == schooladmin.user, "Unexpected user in version"


######################### Unhappy path tests #########################


@pytest.mark.django_db
@pytest.mark.views
def test_delete_teacher_by_another_teacher(teacher_client):
    client, _ = teacher_client
    teacher = TeacherFactory()
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Teacher.objects.filter(id=teacher.id).count() == 1


@pytest.mark.django_db
@pytest.mark.views
def test_delete_teacher_by_user(user_client):
    client, _ = user_client
    teacher = TeacherFactory()
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Teacher.objects.filter(id=teacher.id).count() == 1


@pytest.mark.django_db
@pytest.mark.views
def test_delete_teacher_not_found(school_admin_client):
    client, _ = school_admin_client
    url = reverse('teacher-detail', args=[9999])
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.views
def test_delete_teacher_by_guardian(user_client):
    client, _ = user_client
    teacher = TeacherFactory()
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Teacher.objects.filter(id=teacher.id).count() == 1


@pytest.mark.django_db
@pytest.mark.views
def test_delete_teacher_by_unauthenticated_user():
    client = APIClient()
    teacher = TeacherFactory()
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Teacher.objects.filter(id=teacher.id).count() == 1


@pytest.mark.django_db
@pytest.mark.views
def test_delete_teacher_by_student(student_client):
    client, student = student_client
    teacher = TeacherFactory(school=student.school, classrooms=[student.classroom])
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Teacher.objects.filter(id=teacher.id).count() == 1


@pytest.mark.django_db
@pytest.mark.views
def test_delete_teacher_by_self(teacher_client):
    client, teacher = teacher_client
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert str(response.data['detail']) == "You do not have permission to perform this action."
    assert Teacher.objects.filter(id=teacher.id).count() == 1


@pytest.mark.django_db
@pytest.mark.views
def test_delete_teacher_by_another_school_admin(school_admin_client):
    client, _ = school_admin_client
    teacher = TeacherFactory()
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Teacher.objects.filter(id=teacher.id).count() == 1

