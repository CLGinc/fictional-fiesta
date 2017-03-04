from django.contrib import admin

from .models import Invitation


class InvitationAdmin(admin.ModelAdmin):
    readonly_fields = ('key',)


admin.site.register(Invitation, InvitationAdmin)
