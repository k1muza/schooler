from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .models import Teacher
from .serializers import TeacherSerializer


@api_view(['GET'])
def teacher_list(request):
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, id=pk)
    serializer = TeacherSerializer(teacher, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def teacher_create(request):
    print('logged in user', request.user, request.user.is_authenticated)
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print('errors', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, id=pk)
    serializer = TeacherSerializer(instance=teacher, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    print('errors', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, id=pk)
    teacher.delete()
    return Response("Teacher deleted successfully")


@api_view(['GET'])
def teacher_search(request, search):
    teachers = Teacher.objects.filter(
        Q(user__first_name__icontains=search) | 
        Q(user__last_name__icontains=search) | 
        Q(user__username__icontains=search) |
        Q(user__email__icontains=search)
    )
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)
