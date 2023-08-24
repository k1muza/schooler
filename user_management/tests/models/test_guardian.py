import pytest
from django.contrib import admin
from user_management.models import Guardian
from user_management.tests.factories import GuardianFactory, StudentFactory


@pytest.mark.django_db
def test_create_guardian():
    guardian = GuardianFactory()
    assert guardian is not None
    assert guardian.full_name.startswith('Guardian')


@pytest.mark.django_db
def test_read_guardian():
    guardian = GuardianFactory(full_name='Guardian John Doe')
    retrieved_guardian = Guardian.objects.get(full_name='Guardian John Doe')
    assert retrieved_guardian == guardian


@pytest.mark.django_db
def test_update_guardian():
    guardian = GuardianFactory(full_name='Guardian John Doe')
    guardian.full_name = 'Guardian Jane Doe'
    guardian.save()
    retrieved_guardian = Guardian.objects.get(pk=guardian.pk)
    assert retrieved_guardian.full_name == 'Guardian Jane Doe'


@pytest.mark.django_db
def test_delete_guardian():
    guardian = GuardianFactory()
    guardian_id = guardian.pk
    guardian.delete()
    with pytest.raises(Guardian.DoesNotExist):
        Guardian.objects.get(pk=guardian_id)

@pytest.mark.django_db
def test_student_guardian_relation():
    student = StudentFactory()
    guardian = GuardianFactory(student=student)
    assert guardian in student.guardians.all()

@pytest.mark.django_db
def test_guardian_str():
    guardian = GuardianFactory(full_name='Guardian John Doe')
    assert str(guardian) == 'Guardian John Doe'


def test_guardian_admin_registration():
    assert admin.site._registry.get(Guardian) is not None, 'Guardian is not registered in the admin site'
