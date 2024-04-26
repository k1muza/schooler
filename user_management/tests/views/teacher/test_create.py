import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from reversion.models import Version
from school_management.models import School

from school_management.tests.factories import ClassRoomFactory, SchoolFactory
from user_management.models import Teacher
from user_management.tests.factories import TeacherFactory

####################### Happy path tests #######################

@pytest.mark.django_db
@pytest.mark.views
def test_teacher_create_by_school_admin_201(school_admin_client):
    client, schooladmin = school_admin_client
    user_data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@email.com',
        'first_name': 'Test',
        'last_name': 'User',
    }
    data = {
        'user': user_data,
        'school_id': schooladmin.school.pk,
        'qualifications': 'Ph.D. in Education',
    }
    url = reverse('teacher-list')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Teacher.objects.count() == 1
    teacher = Teacher.objects.first()
    assert teacher.qualifications == data['qualifications']
    assert teacher.user.username == user_data['username']

@pytest.mark.django_db
@pytest.mark.views
def test_teacher_create_by_school_admin_defaults_school(school_admin_client):
    client, schooladmin = school_admin_client
    user_data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@email.com',
        'first_name': 'Test',
        'last_name': 'User',
    }
    data = {
        'user': user_data,
        'qualifications': 'Ph.D. in Education',
    }
    url = reverse('teacher-list')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Teacher.objects.count() == 1
    teacher = Teacher.objects.first()
    assert teacher.school == schooladmin.school


@pytest.mark.django_db
@pytest.mark.views
def test_teacher_create_creates_new_version(school_admin_client):
    client, schooladmin = school_admin_client
    user_data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@email.com',
        'first_name': 'Test',
        'last_name': 'User',
    }
    data = {
        'user': user_data,
        'school_id': schooladmin.school.pk,
        'qualifications': 'Ph.D. in Education',
    }
    url = reverse('teacher-list')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Teacher.objects.count() == 1

    teacher = Teacher.objects.first()
    
    # Test: Check if a version for the created teacher exists
    versions = Version.objects.get_for_object_reference(Teacher, teacher.id)
    assert versions.exists(), "No version found for the created teacher"

    # Assert the user if needed
    last_version = versions.first()
    assert last_version.revision.user == schooladmin.user, "Unexpected user in version"


####################### Unhappy path tests #######################
    
@pytest.mark.django_db
@pytest.mark.views
def test_teacher_create_with_another_teacher_user(school_admin_client):
    client, schooladmin = school_admin_client
    teacher = TeacherFactory()
    user_data = {
        'username': teacher.user.username,
        'password': 'testpass',
        'email': teacher.user.email,
        'first_name': teacher.user.first_name,
        'last_name': teacher.user.last_name,
    }
    data = {
        'user': user_data,
        'school_id': schooladmin.school.pk,
        'qualifications': 'Ph.D. in Education',
    }
    url = reverse('teacher-list')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_409_CONFLICT
    assert Teacher.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.views
def test_teacher_create_with_missing_user(school_admin_client):
    client, schooladmin = school_admin_client
    data = {
        'school_id': schooladmin.school.pk,
        'qualifications': 'Ph.D. in Education',
    }
    url = reverse('teacher-list')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Teacher.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.views
def test_teacher_create_with_invalid_school_id(school_admin_client):
    client, _ = school_admin_client
    user_data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@email.com',
        'first_name': 'Test',
        'last_name': 'User',
    }
    data = {
        'user': user_data,
        'school_id': 99999,
        'qualifications': 'Ph.D. in Education',
    }

    url = reverse('teacher-list')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert f"School with id 99999 does not exist." in str(response.data)
    assert Teacher.objects.count() == 0


####################### Permission tests #######################

@pytest.mark.django_db
@pytest.mark.views
@pytest.mark.parametrize("client_fixture, expected_status", [
    ('school_admin_client', status.HTTP_403_FORBIDDEN),
    ('teacher_client', status.HTTP_403_FORBIDDEN),
    ('student_client', status.HTTP_403_FORBIDDEN),
    ('guardian_client', status.HTTP_403_FORBIDDEN),
])
def test_teacher_create_by_role_403(request, client_fixture, expected_status):
    client, obj = request.getfixturevalue(client_fixture)
    school = SchoolFactory()
    user_data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@email.com',
        'first_name': 'Test',
        'last_name': 'User',
    }
    data = {
        'user': user_data,
        'school_id': school.pk,
        'qualifications': 'Ph.D. in Education',
    }
    url = reverse('teacher-list')
    response = client.post(url, data, format="json")
    assert response.status_code == expected_status
    assert not Teacher.objects.filter(user__username=user_data['username']).exists()


@pytest.mark.django_db
def test_create_by_unauthorized_user_returns_403(user_client):
    client, _ = user_client
    school: School = SchoolFactory()
    user_data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@email.com',
        'first_name': 'Test',
        'last_name': 'User',
    }
    data = {
        'user': user_data,
        'school_id': school.pk,
        'qualifications': 'Ph.D. in Education',
    }
    url = reverse('teacher-list')
    assert Teacher.objects.count() == 0
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Teacher.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.views
def test_teacher_create_validation_error(superuser_client):
    client, _ = superuser_client
    data = {
        'qualifications': 'Ph.D. in Education',
    }
    url = reverse('teacher-list')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'You must specify a school id.' in str(response.data)


@pytest.mark.django_db
@pytest.mark.views
def test_teacher_create_unauthenticated():
    client = APIClient()
    data = {
        'user': {
            'username': 'testuser',
            'password': 'testpass',
            'email': 'test@email.com',
            'first_name': 'Test',
            'last_name': 'User',
        },
        'qualifications': 'Ph.D. in Education',
    }
    url = reverse('teacher-list')
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
