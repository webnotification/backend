# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-27 07:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]