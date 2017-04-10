from django.contrib import admin

from .models import Protocol, Asset, Procedure
from .models import Step, Result, Attachment, DataColumn


class InvitationAdmin(admin.ModelAdmin):
    readonly_fields = ('order',)


admin.site.register(Protocol)
admin.site.register(Asset)
admin.site.register(Procedure)
admin.site.register(Step, InvitationAdmin)
admin.site.register(Result)
admin.site.register(Attachment)
admin.site.register(DataColumn)
