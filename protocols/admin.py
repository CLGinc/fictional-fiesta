from django.contrib import admin

from .models import Protocol, Asset, Result, Attachment

from users.models import Role


class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('last_modified_by', 'protocol', 'datetime_last_modified')


class ResultAdmin(admin.ModelAdmin):
    list_display = ('owner', 'protocol', 'project', 'datetime_created')


class ProtocolAdmin(admin.ModelAdmin):
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


class StepAdmin(admin.ModelAdmin):
    list_display = ('protocol', 'order', 'title')
    ordering = ['procedure__protocol', 'order']

    def protocol(self, obj):
        return obj.procedure.protocol

    protocol.short_description = 'Protocol'


admin.site.register(Protocol, ProtocolAdmin)
admin.site.register(Asset)
admin.site.register(Result, ResultAdmin)
admin.site.register(Attachment)
