from django.contrib import admin

from .models import Researcher, University, Role, Source


class RoleAdmin(admin.ModelAdmin):
    list_display = ('researcher', 'project', 'protocol', 'role')
    search_fields = (
        'researcher__user__username',
        'project__name',
        'protocol__name'
    )
    list_filter = ('role',)


class ResearcherAdmin(admin.ModelAdmin):
    list_display = ('user_first_last_name', 'user_email', 'university')
    search_fields = (
        'researcher__user__username',
        'researcher__user__email',
    )

    def user_first_last_name(self, obj):
        return '{} {}'.format(obj.user.first_name, obj.user.last_name)

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'
    user_first_last_name.short_description = 'Name'


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'researcher', 'isbn', 'url')


admin.site.register(Researcher, ResearcherAdmin)
admin.site.register(University)
admin.site.register(Role, RoleAdmin)
admin.site.register(Source, SourceAdmin)
