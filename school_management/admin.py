from django.contrib import admin

from school_management.models import Class, Level, School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    pass


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    pass


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    pass
