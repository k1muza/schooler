import pytest
from django.contrib import admin
from curriculum_management.models import Syllabus
from curriculum_management.tests.factories import SyllabusFactory
from school_management.tests.factories import LevelFactory


@pytest.mark.django_db
def test_create_syllabus():
    syllabus = SyllabusFactory(levels=[LevelFactory(), LevelFactory()])
    assert Syllabus.objects.count() == 1
    assert syllabus.subject == Syllabus.objects.first().subject
    assert syllabus.levels.count() == 2

@pytest.mark.django_db
def test_read_syllabus():
    syllabus = SyllabusFactory()
    retrieved_syllabus = Syllabus.objects.get(pk=syllabus.pk)
    assert retrieved_syllabus == syllabus

@pytest.mark.django_db
def test_update_syllabus():
    syllabus = SyllabusFactory()
    new_content = "Updated Content"
    syllabus.content = new_content
    syllabus.save()
    retrieved_syllabus = Syllabus.objects.get(pk=syllabus.pk)
    assert retrieved_syllabus.content == new_content

@pytest.mark.django_db
def test_delete_syllabus():
    syllabus = SyllabusFactory()
    syllabus.delete()
    assert Syllabus.objects.count() == 0

def test_syllabus_admin_registration():
    assert admin.site._registry.get(Syllabus) is not None, 'Syllabus is not registered in the admin site'

def test_syllabus_verbose_plural_name():
    assert Syllabus._meta.verbose_name_plural == 'syllabi'
