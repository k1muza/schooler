from rest_framework import serializers
from curriculum_management.models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('name', 'id', 'created_at', 'updated_at',) 
