from django.contrib import admin

from report_management.models import StudentReport


@admin.register(StudentReport)
class StudentReportAdmin(admin.ModelAdmin):
    pass
