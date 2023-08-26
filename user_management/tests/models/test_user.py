import pytest
from django.contrib import admin
from user_management.models import User
from user_management.tests.factories import UserFactory


@pytest.mark.django_db
@pytest.mark.models
def test_create_user():
    user = UserFactory()
    assert user is not None
    assert user.username.startswith('user')


@pytest.mark.django_db
@pytest.mark.models
def test_read_user():
    user = UserFactory.create(username='test_user')
    retrieved_user = User.objects.get(username='test_user')
    assert retrieved_user == user


@pytest.mark.django_db
@pytest.mark.models
def test_read_user():
    user = UserFactory.create(username='test_user')
    retrieved_user = User.objects.get(username='test_user')
    assert retrieved_user == user


@pytest.mark.django_db
@pytest.mark.models
def test_update_user():
    user = UserFactory.create(username='test_user')
    user.username = 'updated_user'
    user.save()
    retrieved_user = User.objects.get(pk=user.pk)
    assert retrieved_user.username == 'updated_user'


@pytest.mark.django_db
@pytest.mark.models
def test_delete_user():
    user = UserFactory.create()
    user_id = user.pk
    user.delete()
    with pytest.raises(User.DoesNotExist):
        User.objects.get(pk=user_id)


@pytest.mark.django_db
@pytest.mark.models
def test_user_str():
    user = UserFactory.create(username='test_user')
    assert str(user) == user.get_full_name()


@pytest.mark.models
def test_user_admin_registration():
    assert admin.site._registry.get(User) is not None, 'User is not registered in the admin site'
