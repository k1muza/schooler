from django.db import transaction
from rest_framework import serializers
from curriculum_management.models import Subject

from school_management.models import ClassRoom, Level, School
from user_management.models import Teacher


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ("__all__")

    def create(self, validated_data):
        school = School.objects.create(**validated_data)
        return school
    
    def update(self, instance, validated_data: dict):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    name = serializers.CharField(
        error_messages={
            'blank': 'Name cannot be empty.',
        }
    )

    class Meta:
        model = Level
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        level = Level.objects.create(**validated_data)
        return level
    
    @transaction.atomic
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    

class ClassroomSerializer(serializers.ModelSerializer):
    school_id = serializers.IntegerField(write_only=True, required=True)
    level_id = serializers.IntegerField(write_only=True, required=True)
    teacher = serializers.SerializerMethodField(method_name='get_teacher_serializer')

    class Meta:
        model = ClassRoom
        fields = '__all__'

    def get_teacher_serializer(self, instance):
        from user_management.serializers import TeacherSerializer
        return TeacherSerializer(instance.teacher).data

    @transaction.atomic
    def create(self, validated_data):        
        classroom = ClassRoom.objects.create(**validated_data)
        return classroom
    
    @transaction.atomic
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
