from django.db import models

class ClassAttendance(models.Model):

    class Status(models.curriculum_managements):
        PRESENT = 'Present'
        ABSENT = 'Absent'

    student = models.ForeignKey('user_management.Student', on_delete=models.CASCADE)
    class_instance = models.ForeignKey('school_management.Class', on_delete=models.CASCADE)
    attendance_date = models.DateField()
    status = models.CharField(max_length=7, choices=Status.choices, default=Status.PRESENT)
