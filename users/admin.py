from django.contrib import admin

from .models import User, Role, Source


class RoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'protocol', 'role')
    search_fields = (
        'username',
        'project__name',
        'protocol__name'
    )
    list_filter = ('role',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'email')
    search_fields = (
        'username',
        'email',
    )


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'isbn', 'url')


admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Source, SourceAdmin)
