import pytest
from user_management.models import Teacher
from user_management.serializers import TeacherSerializer
from user_management.tests.factories import TeacherFactory

@pytest.mark.django_db
def test_teacher_serialization():
    # Create a sample teacher instance (you may want to set up subjects and other fields)
    teacher = TeacherFactory(qualifications="Sample Qualification")

    # Serialize the teacher instance
    serializer = TeacherSerializer(teacher)

    # Check that the serialized data matches the expected output
    assert serializer.data['qualifications'] == "Sample Qualification"
    
    # Add more assertions based on the fields and relations in the Teacher model
