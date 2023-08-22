from factory import SubFactory
from factory.django import DjangoModelFactory
from report_management.models import StudentReport


class StudentReportFactory(DjangoModelFactory):
    class Meta:
        model = StudentReport

    student = SubFactory('user_management.tests.factories.StudentFactory')
    teacher = SubFactory('user_management.tests.factories.TeacherFactory')
    term = SubFactory('curriculum_management.tests.factories.TermFactory')
