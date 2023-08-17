
from exam_management.models import Exam
from factory import SubFactory, Faker
from factory.django import DjangoModelFactory


class ExamFactory(DjangoModelFactory):
    class Meta:
        model = Exam

    subject = SubFactory('curriculum_management.tests.factories.SubjectFactory')
    level = SubFactory('school_management.tests.factories.LevelFactory')
    prepared_by = SubFactory('user_management.tests.factories.TeacherFactory') 
    name = Faker('word')
    date = Faker('date')
    total_score = Faker('random_int', min=0, max=100)


class ExamSeatingFactory(DjangoModelFactory):
    class Meta:
        model = 'exam_management.ExamSeating'

    exam = SubFactory(ExamFactory)
    student = SubFactory('user_management.tests.factories.StudentFactory')
    score = Faker('random_int', min=0, max=100)


class ReportCardFactory(DjangoModelFactory):
    class Meta:
        model = 'exam_management.ReportCard'

    student = SubFactory('user_management.tests.factories.StudentFactory')
    teacher = SubFactory('user_management.tests.factories.TeacherFactory')
    term = SubFactory('curriculum_management.tests.factories.TermFactory')
