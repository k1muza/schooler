import pytest
from django.contrib import admin
from user_management.models import Guardianship
from user_management.tests.factories import GuardianshipFactory, StudentFactory, UserFactory


@pytest.mark.django_db
@pytest.mark.models
def test_create_guardian():
    guardian = GuardianshipFactory(user__username='guardian')
    assert guardian is not None
    assert guardian.user.username == 'guardian'


@pytest.mark.django_db
@pytest.mark.models
def test_read_guardian():
    guardian = GuardianshipFactory(user__username='guardian')
    retrieved_guardian = Guardianship.objects.get(user__username='guardian')
    assert retrieved_guardian == guardian


@pytest.mark.django_db
@pytest.mark.models
def test_update_guardian():
    guardian = GuardianshipFactory(user__username='guardian')
    user = UserFactory()
    guardian.guardian = user
    guardian.save()
    assert Guardianship.objects.get(pk=guardian.pk).guardian == user


@pytest.mark.django_db
@pytest.mark.models
def test_delete_guardian():
    guardian = GuardianshipFactory()
    guardian_id = guardian.pk
    guardian.delete()
    with pytest.raises(Guardianship.DoesNotExist):
        Guardianship.objects.get(pk=guardian_id)


@pytest.mark.django_db
@pytest.mark.models
def test_user_guardian_relation():
    guardian = GuardianshipFactory()
    assert guardian.guardian is not None


@pytest.mark.django_db
@pytest.mark.models
def test_guardian_str():
    guardian = GuardianshipFactory(user__first_name='Guardian John', user__last_name='Doe')
    assert str(guardian) == 'Guardian John Doe'


@pytest.mark.models
def test_guardian_admin_registration():
    assert admin.site._registry.get(Guardianship) is not None, 'Guardian is not registered in the admin site'
