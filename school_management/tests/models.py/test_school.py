import pytest
from django.contrib import admin
from school_management.tests.factories import SchoolFactory
from school_management.models import School


@pytest.mark.django_db
@pytest.mark.models
def test_create_school():
    SchoolFactory()
    assert School.objects.count() == 1

@pytest.mark.django_db
@pytest.mark.models
def test_read_school():
    school = SchoolFactory()
    retrieved_school = School.objects.get(pk=school.pk)
    assert retrieved_school == school

@pytest.mark.django_db
@pytest.mark.models
def test_update_school():
    school = SchoolFactory()
    new_name = "New School Name"
    school.name = new_name
    school.save()
    retrieved_school = School.objects.get(pk=school.pk)
    assert retrieved_school.name == new_name

@pytest.mark.django_db
@pytest.mark.models
def test_delete_school():
    school = SchoolFactory()
    school.delete()
    assert School.objects.count() == 0

@pytest.mark.models
def test_enrolment_admin_registration():
    assert admin.site._registry.get(School) is not None, 'School is not registered in the admin site'
