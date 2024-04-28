import pytest
from django.contrib import admin
from school_management.tests.factories import SchoolFactory
from user_management.models import Administrator
from user_management.tests.factories import AdministratorFactory, UserFactory


@pytest.mark.django_db
@pytest.mark.models
def test_create_school_admin():
    user = UserFactory()
    school_admin = AdministratorFactory(user=user, school__name="Mt Sunset High School")
    assert school_admin.user == user
    assert school_admin.school.name == "Mt Sunset High School"


@pytest.mark.django_db
@pytest.mark.models
def test_read_school_admin():
    school_admin = AdministratorFactory()
    retrieved_school_admin = Administrator.objects.get(id=school_admin.id)
    assert retrieved_school_admin == school_admin


@pytest.mark.django_db
@pytest.mark.models
def test_update_school_admin():
    school_admin = AdministratorFactory.create()
    school = SchoolFactory(name = "Mt Sunset High School")
    school_admin.school = school
    school_admin.save()
    updated_school_admin = Administrator.objects.get(id=school_admin.id)
    assert updated_school_admin.school == school


@pytest.mark.django_db
@pytest.mark.models
def test_delete_school_admin():
    school_admin = AdministratorFactory()
    school_admin_id = school_admin.id
    school_admin.delete()
    with pytest.raises(Administrator.DoesNotExist):
        Administrator.objects.get(id=school_admin_id)


@pytest.mark.django_db
@pytest.mark.models
def test_school_admin_str():
    school_admin = AdministratorFactory()
    assert str(school_admin) == school_admin.user.get_full_name() + " - " + school_admin.school.name


@pytest.mark.models
def test_school_admin_admin_registration():
    assert admin.site._registry.get(Administrator) is not None, 'SchoolAdmin is not registered in the admin site'
