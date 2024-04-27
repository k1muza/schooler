import pytest
from django.contrib import admin
from user_management.models import Student
from user_management.tests.factories import StudentFactory, UserFactory


@pytest.mark.django_db
@pytest.mark.models
def test_create_student():
    user = UserFactory()
    student = StudentFactory(user=user)
    assert student.user == user


@pytest.mark.django_db
@pytest.mark.models
def test_read_student():
    student = StudentFactory()
    retrieved_student = Student.objects.get(pk=student.pk)
    assert student == retrieved_student


@pytest.mark.django_db
@pytest.mark.models
def test_delete_student():
    student = StudentFactory()
    student.delete()
    with pytest.raises(Student.DoesNotExist):
        Student.objects.get(pk=student.pk)


@pytest.mark.django_db
@pytest.mark.models
def test_user_student_relation():
    user = UserFactory()
    student = StudentFactory(user=user)
    assert student.user == user


@pytest.mark.django_db
@pytest.mark.models
def test_student_str():
    student = StudentFactory()
    assert str(student) == student.user.get_full_name()


@pytest.mark.models
def test_student_admin_registration():
    assert admin.site._registry.get(Student) is not None, 'Student is not registered in the admin site'
