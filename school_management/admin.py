from django.contrib import admin

from school_management.models import ClassRoom, Level, School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    pass


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    pass


@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    pass
