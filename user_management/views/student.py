from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from guardian.shortcuts import assign_perm

from user_management.permissions import IsSchoolAdmin, IsTeacherOfStudent
from ..models import Student
from ..serializers import StudentSerializer


@api_view(["GET"])
def list(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def detail(request, pk):
    student = get_object_or_404(Student, id=pk)
    serializer = StudentSerializer(student, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        classroom_id = serializer.validated_data["classroom_id"]

        if (
            hasattr(request.user, "teacher")
            and request.user.teacher.classrooms.filter(id=classroom_id).exists()
        ):
            student_instance = serializer.save()
            assign_perm("change_student", request.user, student_instance)
            assign_perm("view_student", request.user, student_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif (
            hasattr(request.user, "schooladmin")
            and request.user.schooladmin.school.classrooms.filter(
                id=classroom_id
            ).exists()
        ):
            student_instance = serializer.save()
            assign_perm("change_student", request.user, student_instance)
            assign_perm("view_student", request.user, student_instance)
            assign_perm("delete_student", request.user, student_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(
                {"detail": "Not enough permissions."}, status=status.HTTP_403_FORBIDDEN
            )

    print("errors", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def update(request, pk):
    student = get_object_or_404(Student, id=pk)
    serializer = StudentSerializer(instance=student, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    print("errors", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete(request, pk):
    student = get_object_or_404(Student, id=pk)
    student.delete()
    return Response("Student deleted successfully")


@api_view(["GET"])
def search(request, search):
    students = Student.objects.filter(
        Q(user__first_name__icontains=search)
        | Q(user__last_name__icontains=search)
        | Q(user__username__icontains=search)
        | Q(user__email__icontains=search)
    )
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)
