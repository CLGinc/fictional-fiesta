# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0002_project_protocols'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='sources',
            field=models.ManyToManyField(blank=True, related_name='projects', to='users.Source'),
        ),
    ]
