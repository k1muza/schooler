from django.http import HttpRequest
from rest_framework import permissions

from school_management.models import School


class HasGuardianPermission(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view):
        # Basic permission check for authenticated users
        if not (request.user and request.user.is_authenticated):
            return False
        
        if request.user.is_superuser:
            return True

        # Check for specific object permissions depending on the request method
        if request.method == 'POST':
            school_id = request.data.get('school_id')
            if school_id:            
                school = School.objects.get(id=school_id)
                return (
                    request.user.has_perm('user_management.add_guardianship') and 
                    request.user.has_perm('school_management.view_school', school)
                )
        
        return True
    
    def has_object_permission(self, request: HttpRequest, view, obj):
        if request.user.is_superuser:
            return True
        
        base_permission = False
        if request.method in permissions.SAFE_METHODS:
            base_permission = request.user.has_perm('user_management.view_guardianship', obj)
        elif request.method in ['PUT', 'PATCH']:
            base_permission = request.user.has_perm('user_management.change_guardianship', obj)
        elif request.method == 'DELETE':
            base_permission = request.user.has_perm('user_management.delete_guardianship', obj)
        
        return base_permission
