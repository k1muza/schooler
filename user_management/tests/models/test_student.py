import pytest
from django.contrib import admin
from school_management.tests.factories import ClassRoomFactory
from user_management.models import Student
from user_management.tests.factories import StudentFactory, UserFactory


@pytest.mark.django_db
def test_create_student():
    user = UserFactory()
    classroom = ClassRoomFactory()
    student = StudentFactory(user=user, classroom=classroom)
    assert student.user == user
    assert student.classroom == classroom


@pytest.mark.django_db
def test_read_student():
    student = StudentFactory()
    retrieved_student = Student.objects.get(pk=student.pk)
    assert student == retrieved_student


@pytest.mark.django_db
def test_update_student():
    student = StudentFactory()
    new_classroom = ClassRoomFactory()
    student.classroom = new_classroom
    student.save()
    updated_student = Student.objects.get(pk=student.pk)
    assert updated_student.classroom == new_classroom


@pytest.mark.django_db
def test_delete_student():
    student = StudentFactory()
    student.delete()
    with pytest.raises(Student.DoesNotExist):
        Student.objects.get(pk=student.pk)


@pytest.mark.django_db
def test_user_student_relation():
    user = UserFactory()
    student = StudentFactory(user=user)
    assert student.user == user


@pytest.mark.django_db
def test_classroom_student_relation():
    classroom = ClassRoomFactory()
    student = StudentFactory(classroom=classroom)
    assert student in classroom.students.all()


@pytest.mark.django_db
def test_student_str():
    student = StudentFactory()
    assert str(student) == student.user.get_full_name()

def test_student_admin_registration():
    assert admin.site._registry.get(Student) is not None, 'Student is not registered in the admin site'
