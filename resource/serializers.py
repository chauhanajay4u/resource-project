from . import models
from user.models import User
from user.services.user_session_service import UserSessionService
from user.services.user_registration_service import UserRegistrationService
from rest_framework import serializers
from user.utils import NotAcceptableError
from django.conf import settings


class AdminCreateUserResourceSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=100)
    type = serializers.ChoiceField(choices=models.Resources.TYPE_CHOICES)
    user_id = serializers.IntegerField()

    def validate(self, data):
        if not User.objects.filter(id=data["user_id"], is_active=True).exists():
            raise NotAcceptableError("User Not Found", status=404)
        return data

    def save(self):
        models.Resources.objects.create(**self.validated_data)
        return {
            "message": "User Resource created Successfully"
        }


class AdminResourceListSerializer(serializers.Serializer):
    """Serializer for Getting user Resource list"""

    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.SerializerMethodField()
    user_id = serializers.IntegerField()

    def get_type(self, obj):
        return obj.get_type_display()


class CreateUserResourceSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=100)
    type = serializers.ChoiceField(choices=models.Resources.TYPE_CHOICES)

    def save(self, user_id):
        if not self.check_resource_limit(user_id):
            raise NotAcceptableError("Resource Limit Exhasted", status=400)
        self.validated_data["user_id"] = user_id
        models.Resources.objects.create(**self.validated_data)
        return {
            "message": "Resource created Successfully"
        }

    def check_resource_limit(self, user_id):
        user = User.objects.get(id=user_id)
        resource_limit = user.resource_limit
        resource_count = models.Resources.objects.filter(
            user_id=user_id, is_active=True).count()
        if resource_limit is None:
            return True
        if resource_count < resource_limit:
            return True
        return False


class UserResourceListSerializer(serializers.Serializer):
    """Serializer for Getting user Resource list"""

    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return obj.get_type_display()
