import bcrypt
from user import models
from user.services.user_session_service import UserSessionService
from user.utils import NotAcceptableError


class UserRegistrationService(object):
    """Register New User"""

    def __init__(self):
        pass

    def register_user(self, data, role=None, is_admin=False):
        """Get User Registration"""
        user_info = {}

        email = data.get("email").replace(" ", "")
        if not self.is_email_valid(email):
            raise NotAcceptableError("Email already registered", status=400)

        if not role:
            role = data.get("role")
            if role not in ["admin", "user"]:
                raise NotAcceptableError("Invalid Role")
            
        user_info["email"] = email
        user_info["phone"] = data.get("phone").replace(" ", "")
        user_info["name"] = data.get("name").title()
        user_info["role"] = role
        user_info["city"] = data.get("city")
        user_info["resource_limit"] = None
        user_info["country"] = data.get("country")
        user_info["password_hash"] = self.hash_password(data.get("password"))

        user = models.User.objects.create(**user_info)

        if is_admin:
            return {
                "message": "User Created Successfully"
            }
        else:
            return UserSessionService().create_new_session(user)

    def hash_password(self, password):
        """Create hash password for a user by using gensalt"""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), salt)
        # decode encoded password
        hashed_password = hashed_password.decode(encoding='utf-8')
        return hashed_password

    def is_email_valid(self, email):
        """Checking if email is valid"""
        user_email = models.User.objects.filter(
            email=email,
            is_active=True).exists()
        if user_email:
            return False
        return True