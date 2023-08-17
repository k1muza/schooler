import pytest
from django.contrib import admin
from school_management.models import Level
from school_management.tests.factories import LevelFactory


@pytest.mark.django_db
def test_create_level():
    level = LevelFactory()
    assert Level.objects.count() == 1

@pytest.mark.django_db
def test_read_level():
    level = LevelFactory()
    retrieved_level = Level.objects.get(pk=level.pk)
    assert retrieved_level == level

@pytest.mark.django_db
def test_update_level():
    level = LevelFactory()
    new_name = "New Level Name"
    level.name = new_name
    level.save()
    retrieved_level = Level.objects.get(pk=level.pk)
    assert retrieved_level.name == new_name

@pytest.mark.django_db
def test_delete_level():
    level = LevelFactory()
    level.delete()
    assert Level.objects.count() == 0

@pytest.mark.django_db
def test_level_str():
    level = LevelFactory()
    assert str(level) == level.name + ' - ' + level.school.name

def test_level_admin_registration():
    assert admin.site._registry.get(Level) is not None, 'Level is not registered in the admin site'
