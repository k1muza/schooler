from django.db import models

from core.models import TimeStampedModel

class School(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Level(TimeStampedModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    subjects = models.ManyToManyField('curriculum_management.Subject')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name + ' - ' + self.school.name

class ClassRoom(TimeStampedModel):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    teacher = models.ForeignKey('user_management.Teacher', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name + ' - ' + self.level.name + ' - ' + self.level.school.name
