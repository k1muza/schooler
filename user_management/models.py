from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Teacher(User):
    subjects = models.ManyToManyField('curriculum_management.Subject')
    qualifications = models.TextField()

class Student(User):
    related_class = models.ForeignKey('school_management.Class', on_delete=models.CASCADE)
    date_of_birth = models.DateField()

class Enrolment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    related_class = models.ForeignKey('school_management.Class', on_delete=models.CASCADE)
    enrolment_date = models.DateField()
