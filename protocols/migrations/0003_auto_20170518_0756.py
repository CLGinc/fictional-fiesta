# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-18 07:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protocols', '0002_auto_20170511_1136'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='protocol',
            options={'ordering': ['-datetime_created']},
        ),
    ]
