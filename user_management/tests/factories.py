import factory
from faker import Faker
from factory import SubFactory, Sequence
from factory.django import DjangoModelFactory as Factory
from user_management.models import Teacher
from ..models import (
    User,
    Guardianship,
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


class GuardianshipFactory(Factory):
    class Meta:
        model = Guardianship
        skip_postgeneration_save=True

    user = SubFactory(UserFactory)
    guardian = SubFactory(UserFactory)

    @factory.post_generation
    def contacts(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for contact in extracted:
                self.contacts.add(contact)


class StudentFactory(Factory):
    class Meta:
        model = Student
        skip_postgeneration_save=True

    user = SubFactory(UserFactory)
    school = SubFactory('school_management.tests.factories.SchoolFactory')

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


class AdministratorFactory(Factory):
    class Meta:
        model = 'user_management.Administrator'

    user = SubFactory(UserFactory)
    school = SubFactory('school_management.tests.factories.SchoolFactory')
