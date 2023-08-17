import pytest
from exam_management.models import ExamSeating
from exam_management.tests.factories import ExamSeatingFactory
from django.contrib import admin


@pytest.mark.django_db
def test_create_exam_seating():
    seating = ExamSeatingFactory()
    assert ExamSeating.objects.count() == 1

@pytest.mark.django_db
def test_read_exam_seating():
    seating = ExamSeatingFactory()
    retrieved_seating = ExamSeating.objects.get(pk=seating.pk)
    assert retrieved_seating == seating

@pytest.mark.django_db
def test_update_exam_seating():
    seating = ExamSeatingFactory()
    new_score = 95
    seating.score = new_score
    seating.save()
    retrieved_seating = ExamSeating.objects.get(pk=seating.pk)
    assert retrieved_seating.score == new_score

@pytest.mark.django_db
def test_delete_exam_seating():
    seating = ExamSeatingFactory()
    seating.delete()
    assert ExamSeating.objects.count() == 0

def test_exam_seating_admin_registration():
    assert admin.site._registry.get(ExamSeating) is not None, 'ExamSeating is not registered in the admin site'
