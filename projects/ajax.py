from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import Project
from .views import SingleProjectMixin


class GetProtocolsToAdd(TemplateView, SingleProjectMixin):
    template_name = 'protocols_to_add.html'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(GetProtocolsToAdd, self).get_context_data(**kwargs)
        context['protocols_to_add'] = \
            self.request.user.researcher.get_protocols_to_add(self.object)
        return context

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super(
                GetProtocolsToAdd,
                self
            ).get(request, *args, **kwargs)
        return HttpResponseForbidden()


def get_sources_to_add(request, project_uid):
    if request.is_ajax() and request.method == 'GET':
        selected_project = get_object_or_404(Project, unique_id=project_uid)
        researcher = request.user.researcher
        sources_to_add = researcher.get_sources_to_add(selected_project)
        return render(
            request,
            'sources_to_add.html',
            locals()
        )
    else:
        return HttpResponseForbidden()
