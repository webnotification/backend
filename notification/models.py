from __future__ import unicode_literals

from django.db import models

class Notification(models.Model):
    title = models.CharField(max_length=50)
    message = models.CharField(max_length=100)
    url = models.CharField(max_length=50)

class User(models.Model):
    push_key = models.CharField(max_length=100)
    website = models.CharField(max_length=50)

class Group(models.Model):
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=50)

class Notification_Queue(models.Model):
    user_id = models.IntegerField()
    notification_id = models.IntegerField()
    retries = models.IntegerField()

class User_Group(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()

