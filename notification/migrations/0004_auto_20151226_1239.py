# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-26 12:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_auto_20151226_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationresponse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notification.User'),
        ),
    ]
