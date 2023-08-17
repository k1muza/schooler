from faker import Faker
from factory import SubFactory
from factory.django import DjangoModelFactory

from attendance_management.models import ClassAttendance
from user_management.tests.factories import StudentFactory
from school_management.tests.factories import ClassRoomFactory

fake = Faker()

class ClassAttendanceFactory(DjangoModelFactory):
    class Meta:
        model = ClassAttendance

    student = SubFactory(StudentFactory)
    classroom = SubFactory(ClassRoomFactory)
    attendance_date = fake.date()
    status = ClassAttendance.Status.PRESENT
