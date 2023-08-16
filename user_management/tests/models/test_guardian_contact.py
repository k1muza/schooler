import pytest
from django.forms import ValidationError
from django.contrib import admin
from user_management.models import GuardianContact
from user_management.tests.factories import GuardianContactFactory


@pytest.mark.django_db
def test_create_guardian_contact():
    guardian_contact = GuardianContactFactory()
    assert guardian_contact is not None
    assert guardian_contact.contact_type == GuardianContact.ContactType.PHONE


@pytest.mark.django_db
def test_read_guardian_contact():
    guardian_contact = GuardianContactFactory(contact= '123-456-7890')
    retrieved_guardian_contact = GuardianContact.objects.get(contact='123-456-7890')
    assert retrieved_guardian_contact == guardian_contact


@pytest.mark.django_db
def test_update_guardian_contact():
    guardian_contact = GuardianContactFactory()
    guardian_contact.contact = '987-654-3210'
    guardian_contact.save()
    retrieved_guardian_contact = GuardianContact.objects.get(pk=guardian_contact.pk)
    assert retrieved_guardian_contact.contact == '987-654-3210'


@pytest.mark.django_db
def test_delete_guardian_contact():
    guardian_contact = GuardianContactFactory()
    guardian_contact_id = guardian_contact.pk
    guardian_contact.delete()
    with pytest.raises(GuardianContact.DoesNotExist):
        GuardianContact.objects.get(pk=guardian_contact_id)


@pytest.mark.django_db
def test_invalid_contact_type():
    contact = GuardianContactFactory(contact_type='invalid')
    with pytest.raises(ValidationError):
        contact.full_clean()


@pytest.mark.django_db
def test_contact_str():
    contact = GuardianContactFactory(contact='123-456-7890')
    assert str(contact) == 'phone - 123-456-7890'


def test_contact_admin_registration():
    assert admin.site._registry.get(GuardianContact) is not None, 'Guardian contact is not registered in the admin site'
