import pytest
from rest_framework.test import APIClient
from school_management.admin import SchoolAdmin
from school_management.tests.factories import ClassRoomFactory

from user_management.tests.factories import GuardianFactory, SchoolAdminFactory, UserFactory, TeacherFactory, StudentFactory


@pytest.fixture
def user_client():
    client = APIClient()
    user = UserFactory()
    client.force_authenticate(user=user)
    return client, user


@pytest.fixture
def teacher_client():
    client = APIClient()
    teacher = TeacherFactory(classrooms=[ClassRoomFactory() for _ in range(3)])
    client.force_authenticate(user=teacher.user)
    return client, teacher


@pytest.fixture
def school_admin_client():
    client = APIClient()
    school_admin = SchoolAdminFactory()
    client.force_authenticate(user=school_admin.user)
    return client, school_admin


@pytest.fixture
def superuser_client():
    client = APIClient()
    user = UserFactory(is_superuser=True)
    client.force_authenticate(user=user)
    return client, user


@pytest.fixture
def student_client():
    client = APIClient()
    student = StudentFactory()
    client.force_authenticate(user=student.user)
    return client, student


@pytest.fixture
def guardian_client():
    client = APIClient()
    guardian = GuardianFactory(students=[StudentFactory() for _ in range(3)])
    client.force_authenticate(user=guardian.user)
    return client, guardian
