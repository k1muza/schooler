import pytest
from django.contrib import admin
from user_management.models import Teacher
from user_management.tests.factories import TeacherFactory, UserFactory


@pytest.mark.django_db
def test_create_teacher():
    user = UserFactory()
    teacher = Teacher.objects.create(user=user, qualifications="MSc in Physics")
    assert teacher.user == user
    assert teacher.qualifications == "MSc in Physics"


@pytest.mark.django_db
def test_read_teacher():
    teacher = TeacherFactory()
    retrieved_teacher = Teacher.objects.get(id=teacher.id)
    assert retrieved_teacher == teacher



@pytest.mark.django_db
def test_update_teacher():
    teacher = TeacherFactory.create(qualifications="MSc in Physics")
    teacher.qualifications = "PhD in Physics"
    teacher.save()
    updated_teacher = Teacher.objects.get(id=teacher.id)
    assert updated_teacher.qualifications == "PhD in Physics"


@pytest.mark.django_db
def test_delete_teacher():
    teacher = TeacherFactory()
    teacher_id = teacher.id
    teacher.delete()
    with pytest.raises(Teacher.DoesNotExist):
        Teacher.objects.get(id=teacher_id)


# @pytest.mark.django_db
# def test_teacher_subjects_relation():
#     subjects = SubjectFactory.create_batch(3)
#     teacher = TeacherFactory()
#     teacher.subjects.set(subjects)
#     assert list(teacher.subjects.all()) == subjects


@pytest.mark.django_db
def test_teacher_str():
    teacher = TeacherFactory()
    assert str(teacher) == teacher.user.username


def test_teacher_admin_registration():
    assert admin.site._registry.get(Teacher) is not None, 'Teacher is not registered in the admin site'
