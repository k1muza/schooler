import datetime
import factory
import faker
from factory import SubFactory
from factory.django import DjangoModelFactory
from curriculum_management.models import (
    Exercise,
    ExerciseSubmission,
    Subject,
    Syllabus,
    Term,
)
from school_management.tests.factories import ClassRoomFactory
from user_management.tests.factories import StudentFactory, TeacherFactory

fake = faker.Faker()


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
        skip_postgeneration_save=True

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
        skip_postgeneration_save=True

    subject = SubFactory(SubjectFactory)
    classroom = SubFactory(ClassRoomFactory)
    prepared_by = SubFactory(TeacherFactory)
    title = fake.job()
    content = fake.text()
    total_score = fake.random_int(min=10, max=100)

    @factory.post_generation
    def taken_by(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for student in extracted:
                ExerciseSubmissionFactory(exercise=self, student=student)


class ExerciseSubmissionFactory(DjangoModelFactory):
    class Meta:
        model = ExerciseSubmission

    student = SubFactory(StudentFactory)
    exercise = SubFactory(ExerciseFactory)
    score = fake.random_int(min=0, max=100)
