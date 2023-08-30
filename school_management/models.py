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

class ClassRoom(TimeStampedModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classrooms')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='classrooms')
    teacher = models.ForeignKey('user_management.Teacher', on_delete=models.CASCADE, related_name='classrooms')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name + ' - ' + self.level.name + ' - ' + self.school.name
