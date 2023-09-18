from django.db import transaction
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ForeignKey
from school_management.serializers import ClassroomSerializer, SchoolSerializer
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


class TeacherSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    user = CustomUserSerializer(required=False)
    school = SchoolSerializer(read_only=True)
    school_id = serializers.IntegerField(
        write_only=True,
        required=True,
        error_messages={"required": "school_id is required."},
    )

    class Meta:
        model = Teacher
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        if "user" in validated_data:
            user_data = validated_data.pop("user")
            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = User.objects.create_user(**user_serializer.validated_data)
        elif "user_id" in validated_data:
            user = User.objects.get(id=validated_data["user_id"])
        else:
            raise serializers.ValidationError("user or user_id is required")

        validated_data["user"] = user
        teacher = Teacher.objects.create(**validated_data)
        return teacher

    @transaction.atomic
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return instance


class StudentSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    classroom = ClassroomSerializer(read_only=True)
    school = SchoolSerializer(read_only=True)
    user = UserSerializer(required=False)
    user_id = serializers.IntegerField(write_only=True, required=False)
    classroom_id = serializers.IntegerField(
        write_only=True,
        required=True,
        error_messages={"required": "classroom_id is required."},
    )
    school_id = serializers.IntegerField(
        write_only=True,
        required=True,
        error_messages={"required": "school_id is required."},
    )

    class Meta:
        model = Student
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get("instance", None)
        if instance is not None:
            self.fields["classroom_id"].required = False
            self.fields["school_id"].required = False

    def is_valid(self, raise_exception=False):
        is_base_valid = super().is_valid(raise_exception=raise_exception)

        if not is_base_valid and raise_exception:
            raise serializers.ValidationError(self.errors)

        if "user" in self.initial_data and "user_id" in self.initial_data:
            self._errors["user_and_user_id"] = ["user and user_id cannot be passed together."]
        
        if "user_id" in self.initial_data:
            if Student.objects.filter(user_id=self.initial_data["user_id"]).exists():
                self._errors["user_id"] = [f'Student with user_id {self.initial_data["user_id"]} already exists.']     

        # check for unsupported fields
        unsupported_fields = [
            field
            for field in self.initial_data.keys()
            if field not in self.fields.keys()
        ]
        if unsupported_fields:
            self._errors["unsupported_fields"] = [f"Unsupported student fields: {', '.join(unsupported_fields)}"]      
        
        is_valid = not bool(self._errors)

        if self._errors and raise_exception:
            raise serializers.ValidationError(self.errors)

        return is_valid

    @transaction.atomic
    def create(self, validated_data):
        if "user" in validated_data:
            user_data = validated_data.pop("user")
            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = User.objects.create_user(**user_serializer.validated_data)
        elif "user_id" in validated_data:
            user = User.objects.get(id=validated_data["user_id"])
        else:
            raise serializers.ValidationError("user or user_id is required.")

        validated_data["user"] = user

        student = Student.objects.create(**validated_data)
        return student

    @transaction.atomic
    def update(self, instance, validated_data):
        for field_name, field_value in validated_data.items():
            field = Student._meta.get_field(field_name.replace('_id', ''))
            if isinstance(field, ForeignKey):
                try:
                    field.related_model.objects.get(id=field_value)
                except ObjectDoesNotExist:
                    raise serializers.ValidationError(f"{field.related_model.__name__} with id {field_value} does not exist.")
                
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return instance
