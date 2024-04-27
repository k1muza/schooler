import pytest
from django.contrib import admin
from school_management.models import Class
from school_management.tests.factories import ClassFactory


@pytest.mark.django_db
@pytest.mark.models
def test_create_class():
    ClassFactory()
    assert Class.objects.count() == 1

@pytest.mark.django_db
@pytest.mark.models
def test_read_class():
    klass = ClassFactory()
    retrieved_class = Class.objects.get(pk=klass.pk)
    assert retrieved_class == klass

@pytest.mark.django_db
@pytest.mark.models
def test_update_class():
    klass = ClassFactory()
    new_name = "New class Name"
    klass.name = new_name
    klass.save()
    retrieved_class = Class.objects.get(pk=klass.pk)
    assert retrieved_class.name == new_name

@pytest.mark.django_db
@pytest.mark.models
def test_delete_class():
    klass = ClassFactory()
    klass.delete()
    assert Class.objects.count() == 0

@pytest.mark.django_db
@pytest.mark.models
def test_class_str():
    klass = ClassFactory()
    assert str(klass) == klass.name + ' - ' + klass.level.name + ' - ' + klass.school.name

@pytest.mark.models
def test_class_admin_registration():
    assert admin.site._registry.get(Class) is not None, 'Class is not registered in the admin site'
