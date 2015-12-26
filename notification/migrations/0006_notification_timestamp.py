# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-25 15:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0005_notification_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
