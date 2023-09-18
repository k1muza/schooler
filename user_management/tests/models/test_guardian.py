import pytest
from django.contrib import admin
from user_management.models import Guardian
from user_management.tests.factories import GuardianFactory, StudentFactory


@pytest.mark.django_db
@pytest.mark.models
def test_create_guardian():
    guardian = GuardianFactory(user__username='guardian')
    assert guardian is not None
    assert guardian.user.username == 'guardian'


@pytest.mark.django_db
@pytest.mark.models
def test_read_guardian():
    guardian = GuardianFactory(user__username='guardian')
    retrieved_guardian = Guardian.objects.get(user__username='guardian')
    assert retrieved_guardian == guardian


@pytest.mark.django_db
@pytest.mark.models
def test_update_guardian():
    guardian = GuardianFactory(user__username='guardian')
    guardian.occupation = 'Doctor'
    guardian.save()
    retrieved_guardian = Guardian.objects.get(pk=guardian.pk)
    assert retrieved_guardian.occupation == 'Doctor'


@pytest.mark.django_db
@pytest.mark.models
def test_delete_guardian():
    guardian = GuardianFactory()
    guardian_id = guardian.pk
    guardian.delete()
    with pytest.raises(Guardian.DoesNotExist):
        Guardian.objects.get(pk=guardian_id)


@pytest.mark.django_db
@pytest.mark.models
def test_student_guardian_relation():
    student = StudentFactory()
    guardian = GuardianFactory(students=[student])
    assert guardian in student.guardians.all()


@pytest.mark.django_db
@pytest.mark.models
def test_guardian_str():
    guardian = GuardianFactory(user__first_name='Guardian John', user__last_name='Doe')
    assert str(guardian) == 'Guardian John Doe'


@pytest.mark.models
def test_guardian_admin_registration():
    assert admin.site._registry.get(Guardian) is not None, 'Guardian is not registered in the admin site'
