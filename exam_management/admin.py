from django.contrib import admin

from exam_management.models import Exam, ExamSeating, ReportCard


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    pass


@admin.register(ExamSeating)
class ExamSeatingAdmin(admin.ModelAdmin):
    pass


@admin.register(ReportCard)
class ReportCardAdmin(admin.ModelAdmin):
    pass
