from factory import SubFactory
from factory.django import DjangoModelFactory as Factory
from faker import Faker
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


class ClassRoomFactory(Factory):
    class Meta:
        model = ClassRoom

    name = fake.word()
    level = SubFactory(LevelFactory)
    school = SubFactory(SchoolFactory)
    teacher = SubFactory('user_management.tests.factories.TeacherFactory')
