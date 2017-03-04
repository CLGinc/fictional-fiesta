from django.http import HttpResponseForbidden
from django.views.generic.base import TemplateView

from .views import SingleProjectMixin


class GetItemsToAdd(TemplateView, SingleProjectMixin):
    context_key = ''

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(GetItemsToAdd, self).get_context_data(**kwargs)
        context[self.context_key] = \
            self.get_items_to_add()
        return context

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super(
                GetItemsToAdd,
                self
            ).get(request, *args, **kwargs)
        return HttpResponseForbidden()

    def get_items_to_add(self):
        return None


class GetProtocolsToAdd(GetItemsToAdd):
    template_name = 'protocols_to_add.html'
    context_key = 'protocols_to_add'

    def get_items_to_add(self):
        return self.request.user.researcher.get_protocols_to_add(self.object)


class GetSourcesToAdd(GetItemsToAdd):
    template_name = 'sources_to_add.html'
    context_key = 'sources_to_add'

    def get_items_to_add(self):
        return self.request.user.researcher.get_sources_to_add(self.object)
