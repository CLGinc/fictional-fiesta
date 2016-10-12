from django.contrib.auth.models import User
from django.db import models

from projects.models import Project


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

    def get_projects_by_roles(self, roles):
        """
        Returns projects list django query set based on a list of roles.
        """
        return Project.objects.filter(roles__user=self.user, roles__role__in=roles)
