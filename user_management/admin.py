from django.contrib import admin

from user_management.models import Guardianship, Student, Teacher, User, UserContact, Administrator


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass


@admin.register(Guardianship)
class GuardianAdmin(admin.ModelAdmin):
    pass


@admin.register(UserContact)
class UserContactAdmin(admin.ModelAdmin):
    pass


@admin.register(Administrator)
class SchoolAdminAdmin(admin.ModelAdmin):
    pass
