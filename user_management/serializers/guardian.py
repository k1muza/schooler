from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import ForeignKey
from rest_framework import serializers

from curriculum_management.serializers import SubjectSerializer
from school_management.serializers import ClassSerializer, SchoolSerializer
from user_management.models import Guardianship, Student, Teacher, User
from user_management.serializers.user import UserSerializer


class GuardianSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Guardianship
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # if put or patch, then don't require foreign keys
        request = self.context.get('request', None)
        if request and request.method in ['PUT', 'PATCH']:
            self.fields["user_id"].required = False

    def validate_user_id(self, value):
        if self.instance and self.instance.user_id == value:
            return value  # Allow unchanged user_id on updates
        if Guardianship.objects.filter(user_id=value).exists():
            raise serializers.ValidationError("Guardian with specified user_id already exists.")
        return value

    def is_valid(self, raise_exception=False):
        is_base_valid = super().is_valid(raise_exception=raise_exception)

        if not is_base_valid and raise_exception:
            raise serializers.ValidationError(self.errors)

        # Generalized foreign key validation
        for field in Guardianship._meta.fields:
            if isinstance(field, ForeignKey):
                fk_field_name = f"{field.name}_id"  # Construct the name of the FK field in the serializer
                fk_id = self.initial_data.get(fk_field_name, None)
                if fk_id is not None:
                    try:
                        field.related_model.objects.get(id=fk_id)
                    except ObjectDoesNotExist:
                        self._errors[fk_field_name] = [f"{field.related_model.__name__} with id {fk_id} does not exist."]

        if "user" in self.initial_data and "user_id" in self.initial_data:
            self._errors["user_and_user_id"] = ["user and user_id cannot be passed together."]   

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
            user = None

        guardian = Guardianship.objects.create(user=user, **validated_data)
        return guardian
    
    @transaction.atomic
    def update(self, instance, validated_data):
        if "user" in validated_data:
            user_data = validated_data.pop("user")
            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = User.objects.create_user(**user_serializer.validated_data)
        elif "user_id" in validated_data:
            user = User.objects.get(id=validated_data["user_id"])
        else:
            user = None

        instance.user = user
        instance.save()
        return instance
    
    def delete(self, instance):
        instance.delete()
        return instance
