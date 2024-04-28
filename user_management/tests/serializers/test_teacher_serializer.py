import pytest
from user_management.models import Teacher
from user_management.serializers import TeacherSerializer
from user_management.tests.factories import TeacherFactory

@pytest.mark.django_db
def test_teacher_serialization():
    pass
