from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Role, Source


class RoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'protocol', 'role')
    search_fields = (
        'user__username',
        'project__name',
        'protocol__name'
    )
    list_filter = ('role',)


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'isbn', 'url')


admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Source, SourceAdmin)
