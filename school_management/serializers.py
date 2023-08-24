from django.db import transaction
from rest_framework import serializers

from school_management.models import School


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
