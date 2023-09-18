from rest_framework import permissions

from user_management.models import Student, Teacher


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view) or request.user.is_superuser
    

class IsTeacherOfStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, 'teacher'):
            return request.user.teacher.classrooms.filter(id=request.data.get('classroom_id', None)).exists()
        return False
    
    def has_object_permission(self, request, view, obj: Student):
        if not hasattr(request.user, 'teacher'):
            return False
        
        teacher = Teacher.objects.get(user=request.user)
        return obj.teacher == teacher
    

class IsSchoolAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, 'school_admin'):
            return request.user.school_admin.school.pk == request.data.get('school_id', None)
        return False
    
    def has_object_permission(self, request, view, obj: Student):
        if not hasattr(request.user, 'school_admin'):
            return False
        
        return obj.school == request.user.school_admin.school
    

class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):        
        is_authenticated = request.user and request.user.is_authenticated

        if not is_authenticated:
            return False
        
        if view.action in ['update', 'partial_update', 'retrieve', 'list', 'search']:
            return True  # defer to has_object_permission for these actions

        if hasattr(request.user, 'teacher'):
            is_teacher = request.user.teacher.classrooms.filter(
                id=request.data.get('classroom_id', None)
            ).exists()
            if is_teacher:
                return True

        if hasattr(request.user, 'school_admin'):
            is_school_admin = request.user.school_admin.school.pk == request.data.get('school_id', None)
            if is_school_admin:
                return True

        if request.user.is_superuser:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        is_teacher = hasattr(request.user, 'teacher') and obj.teacher == request.user.teacher
        is_school_admin = hasattr(request.user, 'school_admin') and obj.school == request.user.school_admin.school
        is_superuser = request.user.is_superuser

        output = is_teacher or is_school_admin or is_superuser

        if view.action in ['retrieve']:
            is_student = hasattr(request.user, 'student') and obj == request.user.student
            is_guardian = hasattr(request.user, 'guardian') and obj in request.user.guardian.students.all()

            output = output or is_student or is_guardian

        return output
