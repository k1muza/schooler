from django.core.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied

from school_management.models import School
from user_management.models import User
from validators.base import BaseValidator


class SuperuserValidator(BaseValidator):
    def validate(self, request, *args, **kwargs):
        # Implement validation logic for superusers
        if not request.data.get('school_id'):
            raise ValidationError('You must specify a school id.')
        if not School.objects.filter(id=request.data.get('school_id')).exists():
            raise ValidationError(f"School with id {request.data.get('school_id')} does not exist.")


class SchoolAdminValidator(BaseValidator):
    def validate(self, request, *args, **kwargs):
        # Implement validation logic for school admins
        if not request.user.school_admin.school_id == request.data.get('school_id'):
            raise PermissionDenied('You are not authorized to create a teacher for this school.')


class ValidatorFactory:
    @staticmethod
    def get_validator(user: User) -> BaseValidator:
        if user.is_superuser:
            return SuperuserValidator()
        else:
            return SchoolAdminValidator()
