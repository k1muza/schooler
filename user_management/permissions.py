from django.http import HttpRequest
from django.views import View
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
    def has_permission(self, request: HttpRequest, view):        
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
    
    def is_student(self, request: HttpRequest, obj):
        """Check if the user is a student."""
        if hasattr(request.user, 'student'):
            return request.user.student == obj
        return False
    
    def is_guardian(self, request: HttpRequest, obj):
        """Check if the user is a guardian."""
        if hasattr(request.user, 'guardian'):
            return request.user.guardian.students.filter(id=obj.id).exists()
        return False
    
    def is_teacher(self, request: HttpRequest, obj):
        """Check if the user is a teacher."""
        if hasattr(request.user, 'teacher'):
            return request.user.teacher.classrooms.filter(id=obj.classroom.id).exists()
        return False

    def is_school_admin(self, request: HttpRequest, obj):
        """Check if the user is a school admin."""
        if hasattr(request.user, 'school_admin'):
            return request.user.school_admin.school.pk == obj.school.pk
        return False
    
    def can_edit(self, request: HttpRequest, obj):
        """Check if the user has edit or create permissions."""
        is_teacher = self.is_teacher(request, obj)
        is_school_admin = self.is_school_admin(request, obj)
        return is_teacher or is_school_admin

    def can_retrieve(self, request: HttpRequest, obj):
        """Check if the user has retrieve permissions."""
        is_student = self.is_student(request, obj)
        is_guardian = self.is_guardian(request, obj)
        is_teacher = self.is_teacher(request, obj)
        is_school_admin = self.is_school_admin(request, obj)

        return is_student or is_guardian or is_teacher or is_school_admin
    
    def can_delete(self, request: HttpRequest, obj):
        """Check if the user has delete permissions."""
        is_school_admin = self.is_school_admin(request, obj)
        return is_school_admin

    def has_object_permission(self, request: HttpRequest, view, obj):
        if request.user.is_superuser:
            return True
        
        if view.action in ['destroy']:
            return self.can_delete(request, obj)

        if view.action in ['retrieve']:
            return self.can_retrieve(request, obj)
        
        return self.can_edit(request, obj)
