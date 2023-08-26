import pytest
from django.contrib import admin
from curriculum_management.models import Subject
from curriculum_management.tests.factories import SubjectFactory


@pytest.mark.django_db
@pytest.mark.models
def test_create_subject():
    subject = SubjectFactory()
    assert Subject.objects.count() == 1
    assert subject.name == Subject.objects.first().name


@pytest.mark.django_db
@pytest.mark.models
def test_read_subject():
    subject = SubjectFactory()
    retrieved_subject = Subject.objects.get(pk=subject.pk)
    assert retrieved_subject == subject


@pytest.mark.django_db
@pytest.mark.models
def test_update_subject():
    subject = SubjectFactory()
    new_name = "Mathematics"
    subject.name = new_name
    subject.save()
    retrieved_subject = Subject.objects.get(pk=subject.pk)
    assert retrieved_subject.name == new_name


@pytest.mark.django_db
@pytest.mark.models
def test_delete_subject():
    subject = SubjectFactory()
    subject.delete()
    assert Subject.objects.count() == 0


@pytest.mark.models
def test_subject_admin_registration():
    assert admin.site._registry.get(Subject) is not None, 'Subject is not registered in the admin site'


@pytest.mark.django_db
@pytest.mark.models
def test_str_repr():
    subject = SubjectFactory()
    assert str(subject) == subject.name
