from factory import Factory, SubFactory, Sequence
from factory.fuzzy import FuzzyChoice
from faker import Faker
from school_management.tests.factories import ClassRoomFactory
from user_management.models import Teacher
from ..models import User, Guardian, Student

fake = Faker()

class UserFactory(Factory):
    class Meta:
        model = User

    username = Sequence(lambda n: f"user{n}")
    password = fake.password()


class GuardianFactory(Factory):
    class Meta:
        model = Guardian

    full_name = fake.name()
    contact_number = fake.phone_number()


class StudentFactory(Factory):
    class Meta:
        model = Student

    user = SubFactory(UserFactory)
    guardian = SubFactory(GuardianFactory)
    classroom = SubFactory(ClassRoomFactory)


class TeacherFactory(Factory):
    class Meta:
        model = Teacher

    user = SubFactory(UserFactory)
