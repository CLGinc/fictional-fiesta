from django.contrib import admin

from .models import Researcher, University, Role, Source

admin.site.register(Researcher)
admin.site.register(University)
admin.site.register(Role)
admin.site.register(Source)
