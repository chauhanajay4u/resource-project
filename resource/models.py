from django.db import models
from user.models import ActiveModel, User

# Create your models here.


class Resources(ActiveModel):
    """Model to store user info"""
    TYPE_CHOICES = [
        ('BK', 'BOOKS'),
        ('EL', 'ELECTRONICS'),
        ('CL', 'CLOTHES'),
        ('OT', 'OTHERS'),
    ]
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'resources'
