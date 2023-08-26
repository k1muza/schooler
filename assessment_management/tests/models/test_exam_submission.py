import pytest
from assessment_management.models import ExamSubmission
from assessment_management.tests.factories import ExamSubmissionFactory, ExerciseSubmissionFactory
from django.contrib import admin


@pytest.mark.django_db
@pytest.mark.models
def test_create_exam_seating():
    seating = ExamSubmissionFactory()
    assert ExamSubmission.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.models
def test_read_exam_seating():
    seating = ExamSubmissionFactory()
    retrieved_seating = ExamSubmission.objects.get(pk=seating.pk)
    assert retrieved_seating == seating


@pytest.mark.django_db
@pytest.mark.models
def test_update_exam_seating():
    seating = ExamSubmissionFactory()
    new_score = 95
    seating.score = new_score
    seating.save()
    retrieved_seating = ExamSubmission.objects.get(pk=seating.pk)
    assert retrieved_seating.score == new_score


@pytest.mark.django_db
@pytest.mark.models
def test_delete_exam_seating():
    seating = ExamSubmissionFactory()
    seating.delete()
    assert ExamSubmission.objects.count() == 0


@pytest.mark.models
def test_exam_seating_admin_registration():
    assert admin.site._registry.get(ExamSubmission) is not None, 'ExamSubmission is not registered in the admin site'
