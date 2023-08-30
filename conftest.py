import pytest
from rest_framework.test import APIClient
from school_management.admin import SchoolAdmin

from user_management.tests.factories import SchoolAdminFactory, UserFactory, TeacherFactory, StudentFactory


@pytest.fixture
def user_client():
    client = APIClient()
    user = UserFactory()
    client.force_authenticate(user=user)
    return client, user


@pytest.fixture
def teacher_client():
    client = APIClient()
    teacher = TeacherFactory()
    client.force_authenticate(user=teacher.user)
    return client, teacher


@pytest.fixture
def school_admin_client():
    client = APIClient()
    school_admin = SchoolAdminFactory()
    client.force_authenticate(user=school_admin.user)
    return client, school_admin


@pytest.fixture
def student_client():
    client = APIClient()
    student = StudentFactory()
    client.force_authenticate(user=student.user)
    return client
