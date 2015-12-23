from __future__ import unicode_literals
from django.db import models
from django.utils import timezone

class User(models.Model):
    push_key = models.CharField(max_length=200)
    website = models.CharField(max_length=50)

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    website = models.CharField(max_length=50)
    percentage = models.IntegerField(default=100)

class Permission(models.Model):
    pass

class Ask_Permission(models.Model):
    user_id = models.IntegerField()
    ask = models.BooleanField(default=False)

class Notification(models.Model):
    title = models.CharField(max_length=50)
    message = models.CharField(max_length=100)
    target_url = models.CharField(max_length=50)

class Permission_Group(models.Model):
    permission_id = models.IntegerField()
    group_id = models.IntegerField()

class Notification_Group(models.Model):
    notification_id = models.IntegerField()
    group_id = models.IntegerField()

class PermissionResponse(models.Model):
    user_id = models.IntegerField(unique=True)
    permission_id = models.IntegerField()
    action = models.CharField(max_length=10)
    timestamp = models.DateTimeField(default=timezone.now) 

class NotificationResponse(models.Model):
    user_id = models.IntegerField()
    notification_id = models.IntegerField()
    action = models.CharField(max_length=10)
    timestamp = models.DateTimeField(default=timezone.now) 
    class Meta:
        unique_together = ("user_id", "notification_id")

class Notification_Queue(models.Model):
    user_id = models.IntegerField()
    notification_id = models.IntegerField()


    
