from factory import SubFactory, Faker
from factory.django import DjangoModelFactory
from assessment_management.models import ExamSubmission, ExerciseSubmission


class ExerciseSubmissionFactory(DjangoModelFactory):
    class Meta:
        model = ExerciseSubmission

    student = SubFactory('user_management.tests.factories.StudentFactory')
    exercise = SubFactory('curriculum_management.tests.factories.ExerciseFactory')
    score = Faker('pyint', min_value=0, max_value=100)


class ExamSubmissionFactory(DjangoModelFactory):
    class Meta:
        model = ExamSubmission

    exam = SubFactory('curriculum_management.tests.factories.ExamFactory')
    student = SubFactory('user_management.tests.factories.StudentFactory')
    score = Faker('pyint', min_value=0, max_value=100)
