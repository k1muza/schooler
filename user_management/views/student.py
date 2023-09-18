from rest_framework.response import Response
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework import viewsets, status, serializers

from user_management.permissions import CustomPermission
from ..models import Student, User
from ..serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [CustomPermission]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'teacher'):
            return Student.objects.filter(classroom__in=user.teacher.classrooms.all())
        if hasattr(user, 'school_admin'):
            return Student.objects.filter(school=user.school_admin.school)
        if hasattr(user, 'guardian'):
            return user.guardian.students.all()
        if hasattr(user, 'student'):
            return Student.objects.filter(id=user.student.id)
        return Student.objects.all()

    def create(self, request, *args, **kwargs):
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

    def perform_create(self, serializer: StudentSerializer):
        if serializer.is_valid():
            student_instance = serializer.save()
            student_instance.assign_permissions()  
    
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
