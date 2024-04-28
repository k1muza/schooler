import pytest
from rest_framework.test import APIClient
from school_management.admin import SchoolAdmin
from school_management.tests.factories import ClassFactory

from user_management.tests.factories import GuardianshipFactory, AdministratorFactory, UserFactory, TeacherFactory, StudentFactory


@pytest.fixture
def user_client():
    client = APIClient()
    user = UserFactory()
    client.force_authenticate(user=user)
    return client, user


@pytest.fixture
def teacher_client():
    client = APIClient()
    teacher = TeacherFactory(classes=[ClassFactory() for _ in range(3)])
    client.force_authenticate(user=teacher.user)
    return client, teacher


@pytest.fixture
def administrator_client():
    client = APIClient()
    school_admin = AdministratorFactory()
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
