from django.db.models import Q
from guardian.shortcuts import get_objects_for_user
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from school_management.models import School
from user_management.permissions import HasStudentPermission

from ..models import Student, User
from ..serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [HasStudentPermission]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        perms = [
            'view_student',
            'change_student',
            'delete_student',
        ]
        queryset = get_objects_for_user(
            self.request.user, perms, klass=self.queryset, accept_global_perms=False, any_perm=True)
        return queryset

    def create(self, request, *args, **kwargs):
        if not request.data.get('school_id'):
            return Response('No school_id specified.', status=status.HTTP_400_BAD_REQUEST)
        
        if not School.objects.filter(id=request.data.get('school_id')).exists():
            return Response(f'School with id {request.data.get("school_id")} does not exist.', status=status.HTTP_404_NOT_FOUND)
            
        serializer: StudentSerializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            if 'already exists' in str(e):
                return Response(str(e), status=status.HTTP_409_CONFLICT)
            raise e

    def update(self, request, *args, **kwargs):
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
    
    @action(detail=False, methods=['GET'])
    def search(self, request):
        search_param = request.GET.get('search', '')
        students = self.get_queryset().filter(
            Q(user__first_name__icontains=search_param) |
            Q(user__last_name__icontains=search_param) |
            Q(user__username__icontains=search_param) |
            Q(user__email__icontains=search_param)
        )
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
