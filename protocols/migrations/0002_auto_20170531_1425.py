# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 14:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0003_project_sources'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('protocols', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='result',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='results', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='result',
            name='protocol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='protocols.Protocol'),
        ),
        migrations.AddField(
            model_name='protocol',
            name='assets',
            field=models.ManyToManyField(blank=True, related_name='protocols', to='protocols.Asset'),
        ),
        migrations.AddField(
            model_name='protocol',
            name='last_modified_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='procedures', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='protocol',
            name='sources',
            field=models.ManyToManyField(blank=True, related_name='protocols', to='users.Source'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachemnts', to='protocols.Result'),
        ),
    ]
