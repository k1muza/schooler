import reversion
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Q

from core.models import TimeStampedModel, VersionedModel
from school_management.models import School


@reversion.register()
class User(AbstractUser, TimeStampedModel, VersionedModel):
    class Gender(models.TextChoices):
        MALE = "male"
        FEMALE = "female"

    gender = models.CharField(
        max_length=6, choices=Gender.choices, default=Gender.MALE, null=True, blank=True
    )
    profile = models.JSONField(null=True, blank=True)
    guardians = models.ManyToManyField("self", through="Guardianship", symmetrical=False)

    def __str__(self):
        return self.get_full_name() or self.username
    
    @property
    def schools(self) -> QuerySet["School"]:
        """ Schools where the user is an administrator."""
        query = (
            Q(administratorships__user=self) | 
            Q(teacherships__user=self) | 
            Q(studentships__user=self)
        )
        return School.objects.filter(query).distinct()
    
    @property
    def teachers(self) -> QuerySet["Teacher"]:
        """ Teachers who teach user's classes."""
        return Teacher.objects.filter(classes__students__user=self).distinct()
    
    @property
    def students(self) -> QuerySet["Student"]:
        """ Students taught by the user."""
        return Student.objects.filter(classes__teacher__user=self).distinct()
    
    @property
    def administrators(self) -> QuerySet["Administrator"]:
        """ Administrators of the user's school."""
        return Administrator.objects.filter(school__in=self.schools).distinct()


@reversion.register()
class UserImage(TimeStampedModel, VersionedModel):
    image = models.ImageField(upload_to="images/users")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    is_profile_photo = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "is_profile_photo")

    def __str__(self):
        return self.user.get_full_name() + ' - ' + (
            str(self.image.url) + " (Profile Photo)"
            if self.is_profile_photo
            else str(self.image.url)
        )


@reversion.register()
class UserContact(TimeStampedModel, VersionedModel):
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
        return f'{self.user.get_full_name()} - {self.contact_type} - {self.contact}'


@reversion.register()
class Teacher(TimeStampedModel, VersionedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacherships")
    school = models.ForeignKey("school_management.School", on_delete=models.CASCADE, related_name="teacherships")
    subjects = models.ManyToManyField("curriculum_management.Subject")

    class Meta:
        unique_together = ("user", "school")

    def __str__(self):
        return self.user.get_full_name() or self.user.username
    

@reversion.register()
class Student(TimeStampedModel, VersionedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="studentships")
    school = models.ForeignKey("school_management.School", on_delete=models.CASCADE, related_name="studentships")
    student_number = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        unique_together = ("user", "school")

    def __str__(self):
        return self.user.get_full_name()

    @property
    def teachers(self) -> QuerySet[Teacher]:
        """ Return all teachers of the student."""
        return Teacher.objects.filter(classes__students=self).distinct()


@reversion.register()
class Administrator(TimeStampedModel, VersionedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="administratorships")
    school = models.ForeignKey("school_management.School", on_delete=models.CASCADE, related_name="administratorships")

    class Meta:
        unique_together = ("user", "school")

    def __str__(self):
        return (
            (self.user.get_full_name() or self.user.username) + " - " + self.school.name
        )


@reversion.register()
class Guardianship(TimeStampedModel, VersionedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="guardianship")
    guardian = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wards")
    relationship = models.CharField(max_length=200, )

    class Meta:
        unique_together = ("user", "guardian")

    def __str__(self):
        return self.user.get_full_name() or self.user.username
