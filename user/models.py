from django.db import models
from user.utils import Date

# Create your models here.


class ActiveModel(models.Model):
    """Base model to store status of entries"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class User(ActiveModel):
    """Model to store user info"""
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=55, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    resource_limit = models.IntegerField(null=True)
    password_hash = models.CharField(max_length=60, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'user'
        unique_together = ('email', 'is_active')

    def __unicode__(self):
        return "%s__%s" % (str(self.id), str(self.email))


class UserLogin(ActiveModel):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE)
    session_token = models.CharField(
        editable=False, blank=True, null=True, max_length=64)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user_login'

    @classmethod
    def get_session_with(cls, session_token, user_id):
        return UserLogin.objects.filter(session_token=session_token,
            user_id=user_id, is_active=True).order_by('-updated_at').first()

    @classmethod
    def delete_session(cls, session_token, user_id):
        UserLogin.objects.filter(session_token=session_token, user_id=user_id, 
            is_active=True).update(is_active=False, deleted_at=Date.now())

    def __unicode__(self):
        return "%s__%s" % (str(self.user), str(self.session_token))


