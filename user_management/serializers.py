from django.db import transaction
from rest_framework import serializers
from school_management.serializers import SchoolSerializer
from user_management.models import Teacher, User
from curriculum_management.serializers import SubjectSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'gender', 'username', 'is_staff', 'is_active', 'email')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.save()
        return instance
    

class CustomUserSerializer(UserSerializer):
    def __init__(self, instance=None, data=..., **kwargs):
        self.fields['username'].validators = []
        super().__init__(instance, data, **kwargs)


class TeacherSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    user = CustomUserSerializer()
    school = SchoolSerializer()

    class Meta:
        model = Teacher
        fields = ('__all__')

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**user_serializer.validated_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        school_data = validated_data.pop('school')
        
        for key, value in user_data.items():
            setattr(instance.user, key, value)
        instance.user.save()

        for key, value in school_data.items():
            setattr(instance.school, key, value)
        instance.school.save()

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return instance
