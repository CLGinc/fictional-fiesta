from django.contrib import admin

from .models import Protocol, Asset, Procedure
from .models import Step, Result, Attachment, DataColumn


class StepInline(admin.StackedInline):
    model = Step


class ProcedureAdmin(admin.ModelAdmin):
    inlines = [
        StepInline,
    ]


admin.site.register(Protocol)
admin.site.register(Asset)
admin.site.register(Procedure, ProcedureAdmin)
admin.site.register(Step)
admin.site.register(Result)
admin.site.register(Attachment)
admin.site.register(DataColumn)
