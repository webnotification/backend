# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-25 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_auto_20160112_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='push_key',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
