from user import models
import bcrypt
from user.utils import NotAcceptableError, Date
from django.utils.crypto import get_random_string


class UserSessionService(object):

    def __init__(self):
        pass

    def login_user(self, email, password):
        user = models.User.objects.filter(
            email=email, is_active=True).first()
        if user:
            if self.check_password(password, user.password_hash):
                return self.create_new_session(user)
            raise NotAcceptableError("Password does not match", status=401)
        raise NotAcceptableError("User not found", status=404)

    def create_new_session(self, user):
        session = models.UserLogin.objects.create(user_id=user.id,
            session_token=str(user.id) + '_' + get_random_string(length=20))
        return {
            "user_id": user.id,
            "name": user.name,
            "session_token": session.session_token
        }


    def check_password(self, password, hash):
        """Match hashed password for a user"""
        is_password_valid = bcrypt.checkpw(
            password.encode('utf-8'), hash.encode('utf-8'))
        return is_password_valid

    def logout_user(self, session_token, user_id, logout_all=False):
        if logout_all:
            models.UserLogin.objects.filter(user_id=user_id, 
                is_active=True).update(is_active=False, deleted_at=Date.now())
        else:
            models.UserLogin.delete_session(session_token, user_id)
        return {
            "message": "Logout Successful"
        }
