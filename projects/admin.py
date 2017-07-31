from django.contrib import admin

from .models import Project
from users.models import Role


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'datetime_created', 'archived')
    search_fields = ('name',)
    list_filter = ('archived',)

    def owner(self, obj):
        try:
            owner = obj.get_owner()
            return owner
        except Role.DoesNotExist:
            return 'DOES NOT EXIST'

    owner.short_description = 'Owner'


admin.site.register(Project, ProjectAdmin)
