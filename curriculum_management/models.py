from django.db import models
from django.db.models import F, Q
from django.utils import timezone

from core.models import TimeStampedModel


class Subject(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Term(TimeStampedModel):
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


class Syllabus(TimeStampedModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    levels = models.ManyToManyField('school_management.Level')
    content = models.TextField()

    class Meta:
        verbose_name_plural = 'syllabi'

    def __str__(self):
        syllabus_levels = [str(level) for level in self.levels.all()]
        return self.subject.name + ' - ' + ', '.join(syllabus_levels)


class Exercise(TimeStampedModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey('school_management.ClassRoom', on_delete=models.CASCADE)
    taken_by = models.ManyToManyField('user_management.Student', through='assessment_management.ExerciseSubmission')
    prepared_by = models.ForeignKey('user_management.Teacher', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    total_score = models.IntegerField()

    def __str__(self):
        return self.title


class Exam(TimeStampedModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    level = models.ForeignKey('school_management.Level', on_delete=models.CASCADE)
    taken_by = models.ManyToManyField('user_management.Student', through='assessment_management.ExamSubmission')
    prepared_by = models.ForeignKey('user_management.Teacher', on_delete=models.CASCADE)
    taken_on = models.DateTimeField(default=timezone.now,)
    name = models.CharField(max_length=255)
    total_score = models.IntegerField()

    def __str__(self):
        return f'{self.name} - {self.subject.name} - {self.level.name} - {self.taken_on.year}'
