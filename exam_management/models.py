from django.db import models


class Exam(models.Model):
    subject = models.ForeignKey('curriculum_management.Subject', on_delete=models.CASCADE)
    level = models.ForeignKey('school_management.Level', on_delete=models.CASCADE)
    taken_by = models.ManyToManyField('user_management.Student', through='ExamSeating')
    prepared_by = models.ForeignKey('user_management.Teacher', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField()
    total_score = models.IntegerField()


class ExamSeating(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey('user_management.Student', on_delete=models.CASCADE)
    score = models.IntegerField()


class ReportCard(models.Model):
    student = models.ForeignKey('user_management.Student', on_delete=models.CASCADE)
    teacher = models.ForeignKey('user_management.Teacher', on_delete=models.CASCADE)
    term = models.ForeignKey('curriculum_management.Term', on_delete=models.CASCADE)
    subjects = models.ManyToManyField('curriculum_management.Subject')
