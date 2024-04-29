from factory import SubFactory
from factory.django import DjangoModelFactory as Factory
from factory.faker import Faker
from django.contrib.sites.models import Site

from school_management.models import Class, Level, School


class SiteFactory(Factory):
    class Meta:
        model = Site

    name = Faker('company')
    domain = Faker('domain_name')


class SchoolFactory(Factory):
    class Meta:
        model = School

    name = Faker('company')
    site = SubFactory(SiteFactory)


class LevelFactory(Factory):
    class Meta:
        model = Level

    name = Faker('word')


class ClassFactory(Factory):
    class Meta:
        model = Class

    name = Faker('word')
    level = SubFactory(LevelFactory)
    school = SubFactory(SchoolFactory)
    teacher = SubFactory('user_management.tests.factories.TeacherFactory')
