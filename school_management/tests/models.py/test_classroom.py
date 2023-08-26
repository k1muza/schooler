import pytest
from django.contrib import admin
from school_management.models import ClassRoom
from school_management.tests.factories import ClassRoomFactory


@pytest.mark.django_db
@pytest.mark.models
def test_create_classroom():
    ClassRoomFactory()
    assert ClassRoom.objects.count() == 1

@pytest.mark.django_db
@pytest.mark.models
def test_read_classroom():
    classroom = ClassRoomFactory()
    retrieved_classroom = ClassRoom.objects.get(pk=classroom.pk)
    assert retrieved_classroom == classroom

@pytest.mark.django_db
@pytest.mark.models
def test_update_classroom():
    classroom = ClassRoomFactory()
    new_name = "New Classroom Name"
    classroom.name = new_name
    classroom.save()
    retrieved_classroom = ClassRoom.objects.get(pk=classroom.pk)
    assert retrieved_classroom.name == new_name

@pytest.mark.django_db
@pytest.mark.models
def test_delete_classroom():
    classroom = ClassRoomFactory()
    classroom.delete()
    assert ClassRoom.objects.count() == 0

@pytest.mark.django_db
@pytest.mark.models
def test_classroom_str():
    classroom = ClassRoomFactory()
    assert str(classroom) == classroom.name + ' - ' + classroom.level.name + ' - ' + classroom.school.name

@pytest.mark.models
def test_classroom_admin_registration():
    assert admin.site._registry.get(ClassRoom) is not None, 'ClassRoom is not registered in the admin site'
