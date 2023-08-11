import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_create_user():
    # Create a user
    User.objects.create_user(
        username='testuser',
        password='testpassword',
        email='testuser@example.com'
    )

    # Retrieve the user from the database
    retrieved_user = User.objects.get(username='testuser')

    # Check that the user was successfully created
    assert retrieved_user.username == 'testuser'
    assert retrieved_user.email == 'testuser@example.com'
    assert retrieved_user.check_password('testpassword')
