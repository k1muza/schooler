import reversion
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.query import QuerySet
from reversion.models import Version
from guardian.shortcuts import assign_perm

from core.models import TimeStampedModel


@reversion.register
class User(AbstractUser, TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = "male"
        FEMALE = "female"

    gender = models.CharField(
        max_length=6, choices=Gender.choices, default=Gender.MALE, null=True, blank=True
    )

    def __str__(self):
        return self.get_full_name() or self.username


@reversion.register
class UserImage(models.Model):
    image = models.ImageField(upload_to="images/users")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    is_profile_photo = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "is_profile_photo")

    def __str__(self):
        return (
            str(self.image.url) + " (Profile Photo)"
            if self.is_profile_photo
            else str(self.image.url)
        )


@reversion.register
class UserContact(models.Model):
    class ContactType(models.TextChoices):
        PHONE = "phone"
        EMAIL = "email"
        ADDRESS = "address"

    contact_type = models.CharField(
        max_length=7, choices=ContactType.choices, default=ContactType.PHONE
    )
    contact = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")

    def __str__(self):
        return self.contact_type + " - " + self.contact


@reversion.register
class Teacher(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey("school_management.School", on_delete=models.CASCADE)
    subjects = models.ManyToManyField("curriculum_management.Subject")
    qualifications = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


@reversion.register
class Guardian(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    students = models.ManyToManyField("Student")
    occupation = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


@reversion.register
class Student(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(
        "school_management.ClassRoom", on_delete=models.CASCADE, related_name="students"
    )
    school = models.ForeignKey("school_management.School", on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    student_number = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

    @property
    def teacher(self) -> Teacher:
        return self.classroom.teacher

    @property
    def versions(self) -> QuerySet[Version]:
        return Version.objects.get_for_object(self)
    
    @property
    def guardians(self) -> QuerySet[Guardian]:
        return Guardian.objects.filter(students__in=[self])

    def save(self, *args, **kwargs):
        with reversion.create_revision():
            super(Student, self).save(*args, **kwargs)

    def assign_permissions(self):
        assign_perm("change_student", self.teacher.user, self)
        assign_perm("view_student", self.teacher.user, self)

        for school_admin in SchoolAdmin.objects.filter(school=self.school):
            assign_perm("change_student", school_admin.user, self)
            assign_perm("view_student", school_admin.user, self)
            assign_perm("delete_student", school_admin.user, self)


@reversion.register
class SchoolAdmin(TimeStampedModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="school_admin"
    )
    school = models.ForeignKey("school_management.School", on_delete=models.CASCADE)

    def __str__(self):
        return (
            (self.user.get_full_name() or self.user.username) + " - " + self.school.name
        )


@reversion.register
class Enrolment(TimeStampedModel):
    class Status(models.TextChoices):
        ENROLLED = "enrolled"
        WITHDRAWN = "withdrawn"

    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(
        "school_management.ClassRoom",
        on_delete=models.CASCADE,
        related_name="enrolments",
    )
    enrolment_date = models.DateField()

    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.ENROLLED
    )

    def __str__(self):
        return self.student.user.get_full_name() or self.student.user.username
