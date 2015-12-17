from __future__ import unicode_literals
from django.db import models


class User(models.Model):
    push_key = models.CharField(max_length=100)
    website = models.CharField(max_length=50)

class Group(models.Model):
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=50)

class User_Group(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()

class Notification(models.Model):
    title = models.CharField(max_length=50)
    message = models.CharField(max_length=100)
    target_url = models.CharField(max_length=50)

class PermissionResponse(models.Model):
    user_id = models.IntegerField(unique=True)
    action = models.CharField(max_length=10)

class NotificationResponse(models.Model):
    user_id = models.IntegerField()
    notification_id = models.IntegerField()
    action = models.CharField(max_length=10)
    class Meta:
        unique_together = ("user_id", "notification_id")




    
