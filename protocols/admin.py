from django.contrib import admin

from .models import Protocol, Asset, Procedure
from .models import Step, Result, Attachment

from researchers.models import Role


class StepInline(admin.StackedInline):
    model = Step


class ProcedureAdmin(admin.ModelAdmin):
    inlines = [
        StepInline,
    ]
    list_display = ('last_modified_by', 'protocol', 'datetime_last_modified')


class ResultAdmin(admin.ModelAdmin):
    list_display = ('owner', 'protocol', 'project', 'datetime_created')


class ProtocolAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'datetime_created')
    search_fields = ('name',)

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
admin.site.register(Procedure, ProcedureAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Attachment)
