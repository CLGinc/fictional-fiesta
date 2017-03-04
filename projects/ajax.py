from django.http import HttpResponseForbidden
from django.views.generic.base import TemplateView

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


class GetSourcesToAdd(TemplateView, SingleProjectMixin):
    template_name = 'sources_to_add.html'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(GetSourcesToAdd, self).get_context_data(**kwargs)
        context['sources_to_add'] = \
            self.request.user.researcher.get_sources_to_add(self.object)
        return context

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super(
                GetSourcesToAdd,
                self
            ).get(request, *args, **kwargs)
        return HttpResponseForbidden()
