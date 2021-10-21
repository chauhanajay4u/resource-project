from user import models



class UserInfoService(object):
    """A service to get information related to a User"""

    def __init__(self, user_id):
        """Initialize with user id"""
        self.user_id = user_id

        self.user_obj = models.User.objects.filter(
            id=self.user_id,
            is_active=True).first()

    def is_admin(self):
        """checking if the user is admin"""
        if self.user_obj and self.user_obj.role == 'admin':
            return True
        return False