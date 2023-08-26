from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from school_management.models import Level

from school_management.serializers import LevelSerializer

# Create
@api_view(['POST'])
def level_create(request):
    if request.method == 'POST':
        serializer = LevelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Read (List)
@api_view(['GET'])
def level_list(request):
    levels = Level.objects.all()
    serializer = LevelSerializer(levels, many=True)
    return Response(serializer.data)

# Read (Detail)
@api_view(['GET'])
def level_detail(request, pk):
    level = get_object_or_404(Level, pk=pk)
    serializer = LevelSerializer(level)
    return Response(serializer.data)

# Update
@api_view(['PUT'])
def level_update(request, pk):
    level = get_object_or_404(Level, pk=pk)
    serializer = LevelSerializer(level, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete
@api_view(['DELETE'])
def level_delete(request, pk):
    level = get_object_or_404(Level, pk=pk)
    level.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def level_search(request, search):
    levels = Level.objects.filter(
        Q(name__icontains=search)
    )
    serializer = LevelSerializer(levels, many=True)
    return Response(serializer.data)
