from factory import Factory, SubFactory, Sequence
from factory.fuzzy import FuzzyChoice
from faker import Faker
from user_management.tests.factories import TeacherFactory
from ..models import School, Level, ClassRoom

fake = Faker()

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
    teacher = TeacherFactory()

