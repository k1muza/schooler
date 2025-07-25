from django.contrib import admin

from curriculum_management.models import Exam, Exercise, Subject, Syllabus, Term


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    pass


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    pass


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    pass


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    pass
