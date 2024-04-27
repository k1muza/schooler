from django.db import models

class ClassAttendance(models.Model):

    class Status(models.TextChoices):
        PRESENT = 'Present'
        ABSENT = 'Absent'

    student = models.ForeignKey('user_management.Student', on_delete=models.CASCADE)
    klass = models.ForeignKey('school_management.Class', on_delete=models.CASCADE)
    attendance_date = models.DateField()
    status = models.CharField(max_length=7, choices=Status.choices, default=Status.PRESENT)

    def __str__(self):
        return f'{self.student} - {self.klass} - {self.attendance_date}'
