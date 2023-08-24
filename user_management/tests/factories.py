import factory
from faker import Faker
from factory import SubFactory, Sequence
from factory.django import DjangoModelFactory as Factory
from user_management.models import Teacher
from ..models import (
    Enrolment,
    GuardianContact,
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

    student = SubFactory('user_management.tests.factories.StudentFactory')
    full_name = f"Guardian {fake.name()}"
    contact_number = fake.phone_number()


class GuardianContactFactory(Factory):
    class Meta:
        model = GuardianContact

    contact_type = GuardianContact.ContactType.PHONE
    contact = fake.phone_number()
    guardian = SubFactory(GuardianFactory)


class StudentFactory(Factory):
    class Meta:
        model = Student

    user = SubFactory(UserFactory)
    classroom = SubFactory('school_management.tests.factories.ClassRoomFactory')
    school = SubFactory('school_management.tests.factories.SchoolFactory')


class TeacherFactory(Factory):
    class Meta:
        model = Teacher
        skip_postgeneration_save=True

    user = SubFactory(UserFactory)
    qualifications = fake.text()
    school = SubFactory('school_management.tests.factories.SchoolFactory')

    @factory.post_generation
    def subjects(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for subject in extracted:
                self.subjects.add(subject)


class EnrolmentFactory(Factory):
    class Meta:
        model = Enrolment

    student = SubFactory(StudentFactory)
    classroom = SubFactory('school_management.tests.factories.ClassRoomFactory')
    enrolment_date = fake.date()

    status = Enrolment.Status.ENROLLED
