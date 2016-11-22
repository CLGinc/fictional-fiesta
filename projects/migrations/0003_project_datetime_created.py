# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-22 13:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20161031_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='datetime_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
