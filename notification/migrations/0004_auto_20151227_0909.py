# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-27 09:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_auto_20151227_0900'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='group',
            unique_together=set([('name', 'client')]),
        ),
    ]
