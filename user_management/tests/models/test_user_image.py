from urllib.parse import urlencode

from django.db import IntegrityError
import pytest
from user_management.models import UserImage
from user_management.tests.factories import UserFactory, UserImageFactory


@pytest.mark.django_db
def test_create_user_image():
    user_image = UserImageFactory.create()
    assert user_image.pk is not None
    assert user_image.is_profile_photo == False


@pytest.mark.django_db
def test_read_user_image():
    user_image = UserImageFactory(image='http://example.com/image.jpg')
    retrieved_image = UserImage.objects.get(image='http://example.com/image.jpg')
    assert retrieved_image == user_image


@pytest.mark.django_db
def test_update_user_image():
    user_image = UserImageFactory(image='http://example.com/image.jpg')
    user_image.image = 'http://example.com/updated_image.jpg'
    user_image.save()
    retrieved_image = UserImage.objects.get(pk=user_image.pk)
    assert retrieved_image.image == 'http://example.com/updated_image.jpg'


@pytest.mark.django_db
def test_delete_user_image():
    user_image = UserImageFactory()
    user_image_id = user_image.pk
    user_image.delete()
    with pytest.raises(UserImage.DoesNotExist):
        UserImage.objects.get(pk=user_image_id)


@pytest.mark.django_db
def test_unique_user_profile_image():
    user = UserFactory()
    UserImageFactory(user=user, is_profile_photo=True)
    with pytest.raises(IntegrityError):
        UserImageFactory(user=user, is_profile_photo=True)


@pytest.mark.django_db
def test_user_image_str():
    user_image = UserImageFactory(image='http://example.com/image.jpg')
    assert str(user_image) == user_image.image.url


@pytest.mark.django_db
def test_user_profile_image_str():
    user_image = UserImageFactory(image='http://example.com/image.jpg', is_profile_photo=True)
    assert str(user_image) == user_image.image.url + ' (Profile Photo)'
