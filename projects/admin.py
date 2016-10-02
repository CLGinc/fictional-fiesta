from django.contrib import admin

from .models import Source, Project, Role

admin.site.register(Source)
admin.site.register(Project)
admin.site.register(Role)
