import pytest
from django.forms import ValidationError
from django.contrib import admin
from user_management.models import UserContact
from user_management.tests.factories import UserContactFactory


@pytest.mark.django_db
def test_create_user_contact():
    user_contact = UserContactFactory()
    assert user_contact is not None
    assert user_contact.contact_type == UserContact.ContactType.PHONE


@pytest.mark.django_db
@pytest.mark.django_db
def test_read_user_contact():
    user_contact = UserContactFactory(contact='1234567890')
    retrieved_contact = UserContact.objects.get(contact='1234567890')
    assert retrieved_contact == user_contact


@pytest.mark.django_db
def test_update_user_contact():
    user_contact = UserContactFactory(contact='1234567890')
    user_contact.contact = '0987654321'
    user_contact.save()
    retrieved_contact = UserContact.objects.get(pk=user_contact.pk)
    assert retrieved_contact.contact == '0987654321'


@pytest.mark.django_db
def test_delete_user_contact():
    user_contact = UserContactFactory()
    user_contact_id = user_contact.pk
    user_contact.delete()
    with pytest.raises(UserContact.DoesNotExist):
        UserContact.objects.get(pk=user_contact_id)


@pytest.mark.django_db
def test_invalid_contact_type():
    contact = UserContactFactory(contact_type='invalid')
    with pytest.raises(ValidationError):
        contact.full_clean()

@pytest.mark.django_db
def test_user_contact_str():
    user_contact = UserContactFactory()
    assert str(user_contact) == user_contact.contact


@pytest.mark.django_db
def test_user_contact_str():
    user_contact = UserContactFactory()
    assert str(user_contact) == 'phone - ' + user_contact.contact


def test_user_contact_admin_registration():
    assert admin.site._registry.get(UserContact) is not None, 'User contact is not registered in the admin site'
