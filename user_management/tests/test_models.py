import pytest

from .factories import StudentFactory, TeacherFactory, UserFactory


@pytest.mark.django_db
def test_create_user():
    user = UserFactory()
    assert user.username.startswith("user")
    assert user.is_active


@pytest.mark.django_db
def test_create_teacher():
    teacher = TeacherFactory()
    assert teacher.user.username.startswith('user')


@pytest.mark.django_db
def test_create_student():
    student = StudentFactory()
    assert student.user.username.startswith('user')
