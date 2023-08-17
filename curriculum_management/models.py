from django.db import models
from django.db.models import F, Q
from django.utils import timezone


class Subject(models.Model):
    name = models.CharField(max_length=255)


class Term(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(start_date__lte=F('end_date')), 
                name='start_date_before_end_date'
            )
        ]

class Syllabus(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    levels = models.ManyToManyField('school_management.Level')
    content = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subject', 'levels'], 
                name='unique_syllabus'
            )
        ]
        verbose_name_plural = 'syllabi'


class Exercise(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey('school_management.ClassRoom', on_delete=models.CASCADE)
    taken_by = models.ManyToManyField('user_management.Student', through='ExerciseSubmission')
    prepared_by = models.ForeignKey('user_management.Teacher', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    total_score = models.IntegerField()


class ExerciseSubmission(models.Model):
    student = models.ForeignKey('user_management.Student', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField()
