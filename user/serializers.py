from user import models
from user.services.user_session_service import UserSessionService
from user.services.user_registration_service import UserRegistrationService
from rest_framework import serializers
from user.utils import NotAcceptableError
from django.conf import settings



class AuthenticationSerializer(serializers.Serializer):
    session_token = serializers.CharField(max_length=64)
    user_id = serializers.IntegerField()

    def verify_and_update_session(self):
        session_token = self.validated_data.get("session_token")
        user_id = self.validated_data.get("user_id")

        if session_token == settings.ADMIN_SESSION_TOKEN:
            return True

        login_object = models.UserLogin.get_session_with(
            session_token=session_token, user_id=user_id)
        if login_object:
            return True
        return False


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=100)
    password = serializers.CharField(min_length=6, max_length=60)

    def save(self):
        """Create a new login session bbject or return an old one."""
        return UserSessionService().login_user(
            email=self.validated_data.get("email"),
            password=self.validated_data.get("password"))


class UserLogoutSerializer(serializers.Serializer):

    logout_all = serializers.IntegerField(required=False, allow_null=True)

    def save(self, session_token, user_id):
        return UserSessionService().logout_user(session_token, user_id, 
            logout_all=self.validated_data.get("logout_all"))


class UserRegistrationSerializer(serializers.Serializer):
    """Serializer to create new User from Admin"""
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15)
    role = serializers.CharField(required=False, allow_null=True)
    password = serializers.CharField(min_length=6)
    name = serializers.CharField(max_length=60)
    city = serializers.CharField(required=False, max_length=40, \
        allow_null=True, allow_blank=True)
    country = serializers.CharField(required=False, 
        max_length=15, allow_null=True)

    def save(self, role, is_admin):
        return UserRegistrationService().register_user(
            data=self.validated_data, role=role, is_admin=is_admin)


class UserListSerializer(serializers.Serializer):
    """Serializer for Getting user list"""

    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()
    role = serializers.CharField()
    city = serializers.CharField()
    country = serializers.CharField()


class AdminModifyUserSerializer(serializers.Serializer):

    resource_limit = serializers.IntegerField()

    def save(self, user_id):
        user = models.User.objects.filter(id=user_id)
        if user:
            user.update(resource_limit=self.validated_data.get("resource_limit"))
            return {
                "message": "Resource Limit Update Successfully"
            }
        raise NotAcceptableError("User Not Found", status=404)
