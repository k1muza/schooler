import pytest
from django.contrib import admin
from curriculum_management.models import Exam
from curriculum_management.tests.factories import ExamFactory


@pytest.mark.django_db
@pytest.mark.models
def test_create_exam():
    ExamFactory()
    assert Exam.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.models
def test_read_exam():
    exam = ExamFactory()
    retrieved_exam = Exam.objects.get(pk=exam.pk)
    assert retrieved_exam == exam


@pytest.mark.django_db
@pytest.mark.models
def test_update_exam():
    exam = ExamFactory()
    new_name = "New Exam Name"
    exam.name = new_name
    exam.save()
    retrieved_exam = Exam.objects.get(pk=exam.pk)
    assert retrieved_exam.name == new_name


@pytest.mark.django_db
@pytest.mark.models
def test_delete_exam():
    exam = ExamFactory()
    exam.delete()
    assert Exam.objects.count() == 0


@pytest.mark.models
def test_exam_admin_registration():
    assert admin.site._registry.get(Exam) is not None, 'Exam is not registered in the admin site'


@pytest.mark.django_db
@pytest.mark.models
def test_str_repr():
    exam = ExamFactory()
    assert str(exam) == f'{exam.name} - {exam.subject.name} - {exam.level.name} - {exam.taken_on.year}'
