from django.db import models

class School(models.Model):
    name = models.CharField(max_length=255)

class Level(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    subjects = models.ManyToManyField('curriculum_management.Subject')
    name = models.CharField(max_length=255)

class Class(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    teacher = models.ForeignKey('user_management.Teacher', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
