# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-10 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocols', '0011_datacolumn_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datacolumn',
            name='measurement',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='datacolumn',
            name='unit',
            field=models.CharField(max_length=32),
        ),
    ]