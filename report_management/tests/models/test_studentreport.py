import pytest
from curriculum_management.tests.factories import SubjectFactory
from django.contrib import admin
from report_management.models import StudentReport
from report_management.tests.factories import StudentReportFactory
from user_management.tests.factories import TeacherFactory


@pytest.mark.django_db
@pytest.mark.models
def test_create_report_card():
    subjects = [SubjectFactory() for _ in range(3)]
    report_card = StudentReportFactory()
    report_card.subjects.add(*subjects)
    assert StudentReport.objects.count() == 1
    assert report_card.subjects.count() == 3


@pytest.mark.django_db
@pytest.mark.models
def test_read_report_card():
    report_card = StudentReportFactory()
    retrieved_report_card = StudentReport.objects.get(pk=report_card.pk)
    assert retrieved_report_card == report_card


@pytest.mark.django_db
@pytest.mark.models
def test_update_report_card():
    report_card = StudentReportFactory()
    new_teacher = TeacherFactory()
    report_card.teacher = new_teacher
    report_card.save()
    retrieved_report_card = StudentReport.objects.get(pk=report_card.pk)
    assert retrieved_report_card.teacher == new_teacher


@pytest.mark.django_db
@pytest.mark.models
def test_delete_report_card():
    report_card = StudentReportFactory()
    report_card.delete()
    assert StudentReport.objects.count() == 0


@pytest.mark.models
def test_report_card_admin_registration():
    assert admin.site._registry.get(StudentReport) is not None, 'StudentReport is not registered in the admin site'


@pytest.mark.django_db
@pytest.mark.models
def test_str_repr():
    report_card = StudentReportFactory(student__user__first_name="John", student__user__last_name="Doe")
    assert str(report_card) == report_card.student.user.get_full_name()
