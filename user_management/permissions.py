from rest_framework import permissions

from user_management.models import Student, Teacher


class IsTeacherOfStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Student):
        if not hasattr(request.user, 'teacher'):
            return False
        
        teacher = Teacher.objects.get(user=request.user)
        return obj.teacher == teacher
    

class IsSchoolAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Student):
        if not hasattr(request.user, 'school_admin'):
            return False
        
        return obj.school == request.user.school_admin.school
