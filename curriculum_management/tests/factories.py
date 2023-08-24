import datetime
import factory
from django.utils import timezone
from factory import SubFactory, Faker
from factory.django import DjangoModelFactory
from assessment_management.tests.factories import ExerciseSubmissionFactory
from curriculum_management.models import (Exam, Exercise, Subject, Syllabus, Term)
from school_management.tests.factories import ClassRoomFactory
from user_management.tests.factories import TeacherFactory


class SubjectFactory(DjangoModelFactory):
    class Meta:
        model = Subject

    name = factory.Faker("word")


class TermFactory(DjangoModelFactory):
    class Meta:
        model = Term

    name = factory.Faker("word")
    start_date = factory.Faker("date_this_year")
    end_date = factory.LazyAttribute(
        lambda obj: obj.start_date + datetime.timedelta(days=10)
    )


class SyllabusFactory(DjangoModelFactory):
    class Meta:
        model = Syllabus
        skip_postgeneration_save = True

    subject = SubFactory(SubjectFactory)
    content = factory.Faker("text")

    @factory.post_generation
    def levels(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for level in extracted:
                self.levels.add(level)


class ExerciseFactory(DjangoModelFactory):
    class Meta:
        model = Exercise
        skip_postgeneration_save = True

    subject = SubFactory(SubjectFactory)
    classroom = SubFactory(ClassRoomFactory)
    prepared_by = SubFactory(TeacherFactory)
    title = Faker("word")
    content = Faker("text")
    total_score = Faker("pyint", min_value=0, max_value=100)

    @factory.post_generation
    def taken_by(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for student in extracted:
                ExerciseSubmissionFactory(exercise=self, student=student)


class ExamFactory(DjangoModelFactory):
    class Meta:
        model = Exam

    subject = SubFactory("curriculum_management.tests.factories.SubjectFactory")
    level = SubFactory("school_management.tests.factories.LevelFactory")
    prepared_by = SubFactory("user_management.tests.factories.TeacherFactory")
    name = Faker("word")
    taken_on = factory.LazyFunction(timezone.now)
    total_score = Faker("pyint", min_value=0, max_value=100)
