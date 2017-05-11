# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-11 11:36
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=1024)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
