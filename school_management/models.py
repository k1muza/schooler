from django.db import models

from core.models import TimeStampedModel

class School(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Level(TimeStampedModel):
    name = models.CharField(max_length=255)
    subjects = models.ManyToManyField('curriculum_management.Subject')

    def __str__(self):
        return self.name

class Class(TimeStampedModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='classes')
    teacher = models.ForeignKey('user_management.Teacher', on_delete=models.CASCADE, related_name='classes')
    students = models.ManyToManyField('user_management.Student', related_name='classes')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name + ' - ' + self.level.name + ' - ' + self.school.name
