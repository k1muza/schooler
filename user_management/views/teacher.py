import reversion
from django.db.models import Q
from django.http import HttpRequest
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import get_objects_for_user

from school_management.models import School
from user_management.permissions import HasTeacherPermission

from ..models import Teacher, User
from ..serializers import TeacherSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [HasTeacherPermission]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        perms = [
            'view_teacher',
            'change_teacher',
            'delete_teacher',
        ]
        queryset = get_objects_for_user(
            self.request.user, perms, klass=self.queryset, accept_global_perms=False, any_perm=True)
        return queryset

    def create(self, request: HttpRequest, *args, **kwargs):         
        if request.user.is_superuser:
            if not request.data.get('school_id'):
                return Response('You must specify a school id.', status=status.HTTP_400_BAD_REQUEST)

            elif not School.objects.filter(id=request.data.get('school_id')).exists():
                return Response(f'School with id {request.data.get("school_id")} does not exist.', status=status.HTTP_404_NOT_FOUND)
            
        elif not request.data.get('school_id'):
            request.data['school_id'] = request.user.school_admin.school_id

        elif not School.objects.filter(id=request.data.get('school_id')).exists():
            return Response(f'School with id {request.data.get("school_id")} does not exist.', status=status.HTTP_404_NOT_FOUND)

        elif request.user.school_admin.school_id != request.data.get('school_id'):
            return Response('You are not authorized to create a teacher for this school.', status=status.HTTP_403_FORBIDDEN)

        serializer: TeacherSerializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)

            with reversion.create_revision():
                self.perform_create(serializer)
                if hasattr(request, 'user'):
                    reversion.set_user(request.user)
                reversion.set_comment("Created Teacher instance.")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            if 'already exists' in str(e):
                return Response(str(e), status=status.HTTP_409_CONFLICT)
            raise e

    def update(self, request: HttpRequest, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except serializers.ValidationError as e:
            if 'already exists' in str(e):
                return Response(str(e), status=status.HTTP_409_CONFLICT)
            if 'does not exist' in str(e):
                return Response(str(e), status=status.HTTP_404_NOT_FOUND)
            raise e
        except User.DoesNotExist:
            return Response(f'User with id {request.data.get("user_id")} does not exist.', status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request: HttpRequest, *args, **kwargs):
        # Get the object to be deleted
        instance: Teacher = self.get_object()

        # Create a version object for the deleted instance
        with reversion.create_revision() as version:
            instance.save()

            if hasattr(request, 'user'):
                reversion.set_user(request.user)
            reversion.set_comment("Deleted Teacher instance.")

        # Perform the actual deletion
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def search(self, request: HttpRequest):
        search_param = request.GET.get('search', '')
        queryset = self.get_queryset().filter(
            Q(user__first_name__icontains=search_param) |
            Q(user__last_name__icontains=search_param) |
            Q(user__username__icontains=search_param) |
            Q(user__email__icontains=search_param)
        )
        serializer = TeacherSerializer(queryset, many=True)
        return Response(serializer.data)
