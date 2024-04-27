import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from reversion.models import Version

from school_management.tests.factories import SchoolFactory
from user_management.models import Teacher
from user_management.tests.factories import TeacherFactory


######################### Happy path tests #########################

@pytest.mark.parametrize("client_fixture, expected_status", [
    ('superuser_client', status.HTTP_201_CREATED),
    ('schooladmin_client', status.HTTP_201_CREATED),
])
@pytest.mark.django_db
@pytest.mark.views
def test_delete_teacher_by_priviledged_admin(client_fixture, expected_status, request):
    client, admin = request.getfixturevalue(client_fixture)
    kwargs = {
        'school': admin.school if hasattr(admin, 'school') else SchoolFactory()
    }
    teacher = TeacherFactory(**kwargs)
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Teacher.objects.filter(id=teacher.id).count() == 0


@pytest.mark.django_db
def test_delete_teacher_creates_version(schooladmin_client):
    client, schooladmin = schooladmin_client
    teacher = TeacherFactory(school=schooladmin.school)
    
    assert Teacher.objects.filter(user=teacher.user).exists()

    url = reverse('teacher-detail', args=[teacher.id])
    response = client.delete(url)
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Teacher.objects.filter(id=teacher.id).count() == 0
    
    versions = Version.objects.get_for_object_reference(Teacher, teacher.id)
    assert versions.exists(), "No version found for the deleted teacher"
    
    last_version = versions.first()
    assert last_version.revision.user == schooladmin.user, "Unexpected user in version"


######################### Perm tests #########################

@pytest.mark.parametrize("client_fixture, expected_status", [
    ('schooladmin_client', status.HTTP_404_NOT_FOUND),
    ('teacher_client', status.HTTP_404_NOT_FOUND),
    ('student_client', status.HTTP_404_NOT_FOUND),
    ('guardian_client', status.HTTP_404_NOT_FOUND),
    ('user_client', status.HTTP_404_NOT_FOUND),
])
@pytest.mark.django_db
@pytest.mark.views
def test_delete_teacher_by_unpriv_user(client_fixture, expected_status, request):
    client, _ = request.getfixturevalue(client_fixture)
    teacher = TeacherFactory()
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.delete(url)
    assert response.status_code == expected_status
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
def test_delete_teacher_by_self(teacher_client):
    client, teacher = teacher_client
    url = reverse('teacher-detail', args=[teacher.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert str(response.data['detail']) == "You do not have permission to perform this action."
    assert Teacher.objects.filter(id=teacher.id).count() == 1


######################### Edge cases #########################

@pytest.mark.django_db
@pytest.mark.views
def test_delete_of_nonexisting_teacher(superuser_client):
    client, _ = superuser_client
    url = reverse('teacher-detail', args=[9999])
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
