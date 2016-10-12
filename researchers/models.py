from django.contrib.auth.models import User
from django.db import models


class University(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Universities'

    def __str__(self):
        return self.name


class Researcher(models.Model):
    user = models.OneToOneField(User, related_name='researcher')
    university = models.ForeignKey(University, related_name='researchers')
    scientific_degree = models.CharField(max_length=255)


    def __str__(self):
        return '{} {}'.format(self.scientific_degree, self.user.first_name, self.user.last_name)
