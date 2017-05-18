from django.contrib import admin

from .models import Invitation


class InvitationAdmin(admin.ModelAdmin):
    list_display = (
        'inviter',
        'invited',
        'email',
        'protocol',
        'project',
        'role',
        'accepted',
        'datetime_created')
    search_fields = ('email',)


admin.site.register(Invitation, InvitationAdmin)
