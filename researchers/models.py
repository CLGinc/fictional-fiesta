from django.contrib.auth.models import User
from django.db import models

from projects.models import Role


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

    def get_roles(self, scope=None, role_names=[role[0] for role in Role._meta.get_field('role').choices]):
        """
        Returns roles list django query set based on scope and a list of role names.
        If no role names are specified all roles are selected.
        Scope defines if the query gets roles for projects, protocols or both.
        """
        if scope == 'project':
            return Role.objects.filter(
                user=self.user,
                role__in=role_names,
                protocol=None
                ).exclude(project=None).select_related(scope)
        elif scope == 'protocol':
            return Role.objects.filter(
                user=self.user,
                role__in=role_names,
                project=None
                ).exclude(protocol=None).select_related(scope)
        else:
            return Role.objects.filter(
                user=self.user,
                role__in=role_names,).select_related('project', 'protocol')
