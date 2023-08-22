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
        verbose_name_plural = 'syllabi'


class Exercise(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey('school_management.ClassRoom', on_delete=models.CASCADE)
    taken_by = models.ManyToManyField('user_management.Student', through='assessment_management.ExerciseSubmission')
    prepared_by = models.ForeignKey('user_management.Teacher', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    total_score = models.IntegerField()


class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    level = models.ForeignKey('school_management.Level', on_delete=models.CASCADE)
    taken_by = models.ManyToManyField('user_management.Student', through='assessment_management.ExamSubmission')
    prepared_by = models.ForeignKey('user_management.Teacher', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField()
    total_score = models.IntegerField()
