
from django.db import transaction
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ForeignKey
from school_management.serializers import ClassSerializer, SchoolSerializer
from user_management.models import Student, Teacher, User
from curriculum_management.serializers import SubjectSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "gender",
            "username",
            "is_staff",
            "is_active",
            "email",
        )

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.save()
        return instance


class CustomUserSerializer(UserSerializer):
    def __init__(self, instance=None, data=..., **kwargs):
        self.fields["username"].validators = []
        super().__init__(instance, data, **kwargs)

