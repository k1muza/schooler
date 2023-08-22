from django.contrib import admin

from assessment_management.models import ExamSubmission


@admin.register(ExamSubmission)
class ExamSubmissionAdmin(admin.ModelAdmin):
    pass
