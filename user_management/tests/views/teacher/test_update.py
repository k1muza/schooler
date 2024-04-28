import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from school_management.tests.factories import SchoolFactory
from user_management.tests.factories import TeacherFactory

################################ Happy paths #####################################

@pytest.mark.django_db
@pytest.mark.views
def test_teacher_update_by_superuser_200(superuser_client):
    client, _ = superuser_client
    teacher = TeacherFactory()

    url = reverse("teacher-detail", args=[teacher.id])
    updated_data = {
        "school_id": teacher.school.id,
        "user_id": teacher.user.id,
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    teacher.refresh_from_db()


@pytest.mark.django_db
@pytest.mark.views
def test_teacher_update_by_school_admin_200(administrator_client):
    client, school_admin = administrator_client
    teacher = TeacherFactory(school=school_admin.school)

    url = reverse("teacher-detail", args=[teacher.id])
    updated_data = {
        "school_id": teacher.school.id,
        "user_id": teacher.user.id,
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    teacher.refresh_from_db()


@pytest.mark.django_db
@pytest.mark.views
def test_teacher_update_by_teacher_200(teacher_client):
    client, teacher = teacher_client

    url = reverse("teacher-detail", args=[teacher.id])
    updated_data = {
        "school_id": teacher.school.id,
        "user_id": teacher.user.id,
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    teacher.refresh_from_db()


########################## Permission tests #############################


@pytest.mark.django_db
@pytest.mark.views
@pytest.mark.parametrize("client_fixture, expected_status", [
    ('administrator_client', status.HTTP_404_NOT_FOUND),
    ('teacher_client', status.HTTP_404_NOT_FOUND),
    ('student_client', status.HTTP_404_NOT_FOUND),
])
def test_teacher_update_by_role_404(request, client_fixture, expected_status):
    client, _ = request.getfixturevalue(client_fixture)
    teacher = TeacherFactory()

    url = reverse("teacher-detail", args=[teacher.id])
    updated_data = {
        "school_id": teacher.school.id,
        "user_id": teacher.user.id,
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == expected_status
    teacher.refresh_from_db()


@pytest.mark.django_db
@pytest.mark.views
def test_teacher_update_unauthenticated():
    teacher = TeacherFactory()
    client = APIClient()
    url = reverse("teacher-detail", args=[teacher.id])
    response = client.put(url, {}, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.views
def test_teacher_update_not_found(user_client):
    client, _ = user_client
    url = reverse("teacher-detail", args=[999])
    response = client.put(url, {}, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.views
def test_teacher_update_immutable_school_id(superuser_client):
    client, _ = superuser_client
    teacher = TeacherFactory()

    original_school = teacher.school
    school = SchoolFactory()

    url = reverse("teacher-detail", args=[teacher.id])
    updated_data = {
        "school_id": school.id,
        "user_id": teacher.user.id,
    }
    response = client.put(url, updated_data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    teacher.refresh_from_db()
    assert teacher.school == original_school
