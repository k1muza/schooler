import datetime
import factory
from faker import Faker
from factory import SubFactory, Sequence
from factory.django import DjangoModelFactory as Factory
from user_management.models import Teacher
from ..models import (
    User,
    Guardian,
    Student,
    UserContact,
    UserImage,
)

fake = Faker()


class UserFactory(Factory):
    class Meta:
        model = User

    username = Sequence(lambda n: f"user{n}")
    password = fake.password()
    gender = User.Gender.FEMALE
    first_name = fake.first_name()
    last_name = fake.last_name()


class UserContactFactory(Factory):
    class Meta:
        model = UserContact

    contact_type = UserContact.ContactType.PHONE
    contact = fake.phone_number()
    user = SubFactory(UserFactory)


class UserImageFactory(Factory):
    class Meta:
        model = UserImage

    user = SubFactory(UserFactory)
    image = fake.image_url()
    is_profile_photo = False


class GuardianFactory(Factory):
    class Meta:
        model = Guardian
        skip_postgeneration_save=True

    user = SubFactory(UserFactory)
    occupation = factory.Faker('job')

    @factory.post_generation
    def contacts(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for contact in extracted:
                self.contacts.add(contact)

    @factory.post_generation
    def students(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for student in extracted:
                self.students.add(student)


class StudentFactory(Factory):
    class Meta:
        model = Student
        skip_postgeneration_save=True

    user = SubFactory(UserFactory)
    school = SubFactory('school_management.tests.factories.SchoolFactory')
    date_of_birth = factory.Faker('date_between_dates', date_start=datetime.date(2012, 1, 1), date_end=datetime.date(2015, 12, 31))

    @factory.post_generation
    def guardians(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for guardian in extracted:
                guardian.students.add(self)


class TeacherFactory(Factory):
    class Meta:
        model = Teacher
        skip_postgeneration_save=True

    user = SubFactory(UserFactory)
    qualifications = fake.text()
    school = SubFactory('school_management.tests.factories.SchoolFactory')

    @factory.post_generation
    def classes(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for klass in extracted:
                self.classes.add(klass)

    @factory.post_generation
    def subjects(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for subject in extracted:
                self.subjects.add(subject)


class SchoolAdminFactory(Factory):
    class Meta:
        model = 'user_management.SchoolAdmin'

    user = SubFactory(UserFactory)
    school = SubFactory('school_management.tests.factories.SchoolFactory')
