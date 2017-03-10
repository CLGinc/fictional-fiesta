from django.contrib import admin
from adminsortable.admin import NonSortableParentAdmin, SortableStackedInline

from .models import Protocol, Asset, Procedure
from .models import Step, Result, Attachment, DataColumn


class StepInline(SortableStackedInline):
    model = Step
    extra = 1


class ProcedureAdmin(NonSortableParentAdmin):
    inlines = [StepInline]


admin.site.register(Protocol)
admin.site.register(Asset)
admin.site.register(Procedure, ProcedureAdmin)
admin.site.register(Step)
admin.site.register(Result)
admin.site.register(Attachment)
admin.site.register(DataColumn)
