from django.contrib.auth.models import User
from django.db import models


class University(models.Model):
    name = models.CharField(max_length=255)


class Researcher(models.Model):
    user = models.ForeignKey(User, related_name='researchers')
    university = models.ForeignKey(University, related_name='researchers')
    scientific_degree = models.CharField(max_length=255)
