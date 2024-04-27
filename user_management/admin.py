from django.contrib import admin

from user_management.models import Guardian, Student, Teacher, User, UserContact, SchoolAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    pass


@admin.register(UserContact)
class UserContactAdmin(admin.ModelAdmin):
    pass


@admin.register(SchoolAdmin)
class SchoolAdminAdmin(admin.ModelAdmin):
    pass
