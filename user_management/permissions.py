from django.db import models
from django.http import HttpRequest
from rest_framework import permissions
from django.views import generic

from school_management.models import School


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view) or request.user.is_superuser
    

class HasTeacherPermission(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view: generic.View):
        # Basic permission check for authenticated users
        if not (request.user and request.user.is_authenticated):
            return False
        
        if request.user.is_superuser:
            return True

        # Check for specific object permissions depending on the request method
        if request.method == 'POST':
            return request.user.has_perm('user_management.add_teacher')
        
        return True
    
    def has_object_permission(self, request: HttpRequest, view: generic.View, obj: models.Model):
        if request.user.is_superuser:
            return True
        
        # Check for specific object permissions depending on the request method
        if request.method in permissions.SAFE_METHODS:
            return request.user.has_perm('user_management.view_teacher', obj)
        elif request.method in ['PUT', 'PATCH']:
            return request.user.has_perm('user_management.change_teacher', obj)
        elif request.method == 'DELETE':
            return request.user.has_perm('user_management.delete_teacher', obj)
        return False
    

class HasStudentPermission(permissions.BasePermission):
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
                    request.user.has_perm('user_management.add_student') and 
                    request.user.has_perm('school_management.view_school', school)
                )
        
        return True
    
    def has_object_permission(self, request: HttpRequest, view, obj):
        if request.user.is_superuser:
            return True
        
        base_permission = False
        if request.method in permissions.SAFE_METHODS:
            base_permission = request.user.has_perm('user_management.view_student', obj)
        elif request.method in ['PUT', 'PATCH']:
            base_permission = request.user.has_perm('user_management.change_student', obj)
        elif request.method == 'DELETE':
            base_permission = request.user.has_perm('user_management.delete_student', obj)
        
        return base_permission and request.user.has_perm('school_management.view_school', obj.school)
