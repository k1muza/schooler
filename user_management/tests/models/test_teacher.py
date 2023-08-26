import pytest
from curriculum_management.tests.factories import SubjectFactory
from django.contrib import admin
from user_management.models import Teacher
from user_management.tests.factories import TeacherFactory, UserFactory


@pytest.mark.django_db
@pytest.mark.models
def test_create_teacher():
    user = UserFactory()
    subjects = [SubjectFactory() for _ in range(3)]
    teacher = TeacherFactory(user=user, qualifications="MSc in Physics", subjects=subjects)
    assert teacher.user == user
    assert teacher.qualifications == "MSc in Physics"


@pytest.mark.django_db
@pytest.mark.models
def test_read_teacher():
    teacher = TeacherFactory()
    retrieved_teacher = Teacher.objects.get(id=teacher.id)
    assert retrieved_teacher == teacher


@pytest.mark.django_db
@pytest.mark.models
def test_update_teacher():
    teacher = TeacherFactory.create(qualifications="MSc in Physics")
    teacher.qualifications = "PhD in Physics"
    teacher.save()
    updated_teacher = Teacher.objects.get(id=teacher.id)
    assert updated_teacher.qualifications == "PhD in Physics"


@pytest.mark.django_db
@pytest.mark.models
def test_delete_teacher():
    teacher = TeacherFactory()
    teacher_id = teacher.id
    teacher.delete()
    with pytest.raises(Teacher.DoesNotExist):
        Teacher.objects.get(id=teacher_id)


@pytest.mark.django_db
@pytest.mark.models
def test_teacher_str():
    teacher = TeacherFactory()
    assert str(teacher) == teacher.user.get_full_name()


@pytest.mark.models
def test_teacher_admin_registration():
    assert admin.site._registry.get(Teacher) is not None, 'Teacher is not registered in the admin site'
