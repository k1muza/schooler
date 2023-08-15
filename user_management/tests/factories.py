from factory import Factory, SubFactory, Sequence
from factory.fuzzy import FuzzyChoice
from faker import Faker
from user_management.models import Teacher
from ..models import User, Guardian, Student
from school_management.models import School, Level, ClassRoom

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


class SchoolFactory(Factory):
    class Meta:
        model = School

    name = fake.company()


class LevelFactory(Factory):
    class Meta:
        model = Level

    name = fake.word()
    school = SubFactory(SchoolFactory)


class ClassRoomFactory(Factory):
    class Meta:
        model = ClassRoom

    name = fake.word()
    level = SubFactory(LevelFactory)


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
