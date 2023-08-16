from django.contrib import admin

from user_management.models import Enrolment, Guardian, GuardianContact, Student, Teacher, User, UserContact


admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Guardian)
admin.site.register(Enrolment)
admin.site.register(UserContact)
admin.site.register(GuardianContact)
