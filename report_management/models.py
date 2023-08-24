from django.db import models

from core.models import TimeStampedModel

class StudentReport(TimeStampedModel):
    student = models.ForeignKey('user_management.Student', on_delete=models.CASCADE)
    teacher = models.ForeignKey('user_management.Teacher', on_delete=models.CASCADE)
    term = models.ForeignKey('curriculum_management.Term', on_delete=models.CASCADE)
    subjects = models.ManyToManyField('curriculum_management.Subject')

    def __str__(self):
        return self.student.user.get_full_name()
