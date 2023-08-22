from django.db import models
from django.utils import timezone


class ExerciseSubmission(models.Model):
    student = models.ForeignKey('user_management.Student', on_delete=models.CASCADE)
    exercise = models.ForeignKey('curriculum_management.Exercise', on_delete=models.CASCADE)
    submission_date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField()


class ExamSubmission(models.Model):
    exam = models.ForeignKey('curriculum_management.Exam', on_delete=models.CASCADE)
    student = models.ForeignKey('user_management.Student', on_delete=models.CASCADE)
    score = models.IntegerField()
