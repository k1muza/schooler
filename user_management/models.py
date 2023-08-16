from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = 'male'
        FEMALE = 'female'

    gender = models.CharField(max_length=6, choices=Gender.choices, default=Gender.MALE, null=True, blank=True)

    def __str__(self):
        return self.get_full_name() or self.username


class UserImage(models.Model):
    image = models.ImageField(upload_to="images/users")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    is_profile_photo = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'is_profile_photo')

    def __str__(self):
        return str(self.image.url) + ' (Profile Photo)' if self.is_profile_photo else str(self.image.url)


class UserContact(models.Model):
    class ContactType(models.TextChoices):
        PHONE = 'phone'
        EMAIL = 'email'
        ADDRESS = 'address'

    contact_type = models.CharField(max_length=7, choices=ContactType.choices, default=ContactType.PHONE)
    contact = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')

    def __str__(self):
        return self.contact_type + ' - ' + self.contact


class Teacher(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subjects = models.ManyToManyField('curriculum_management.Subject')
    qualifications = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Guardian(TimeStampedModel):
    full_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name
    

class GuardianContact(models.Model):
    class ContactType(models.TextChoices):
        PHONE = 'phone'
        EMAIL = 'email'
        ADDRESS = 'address'

    contact_type = models.CharField(max_length=7, 
                                    choices=ContactType.choices, 
                                    default=ContactType.PHONE)
    
    contact = models.CharField(max_length=200)
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE, related_name='contacts')

    def __str__(self):
        return self.contact_type + ' - ' + self.contact


class Student(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey('school_management.ClassRoom', on_delete=models.CASCADE, related_name='students')
    guardian = models.ForeignKey(Guardian, on_delete=models.PROTECT, related_name='students')
    date_of_birth = models.DateField(null=True, blank=True)
    student_number = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Enrolment(TimeStampedModel):
    class Status(models.TextChoices):
        ENROLLED = 'enrolled'
        WITHDRAWN = 'withdrawn'

    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey('school_management.ClassRoom', on_delete=models.CASCADE, related_name='enrolments')
    enrolment_date = models.DateField()

    status = models.CharField(max_length=15, choices=Status.choices, default=Status.ENROLLED)

    def __str__(self):
        return self.student.user.get_full_name() or self.student.user.username
