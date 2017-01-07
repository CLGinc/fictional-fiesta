# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-07 13:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('protocols', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scientific_degree', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('owner', 'Owner'), ('contributor', 'Contributor'), ('watcher', 'Watcher')], max_length=255)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='projects.Project')),
                ('protocol', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='protocols.Protocol')),
                ('researcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='researchers.Researcher')),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(blank=True, max_length=255, null=True)),
                ('isbn', models.CharField(blank=True, max_length=255, null=True)),
                ('researcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sources', to='researchers.Researcher')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Universities',
            },
        ),
        migrations.AddField(
            model_name='researcher',
            name='university',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='researchers', to='researchers.University'),
        ),
        migrations.AddField(
            model_name='researcher',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='researcher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together=set([('researcher', 'protocol'), ('researcher', 'project')]),
        ),
    ]
