# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-27 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
