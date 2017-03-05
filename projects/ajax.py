from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.views.generic.edit import FormView

from .views import SingleProjectMixin
from .forms import AddElementsForm


class GetItemsToAdd(FormView, SingleProjectMixin):
    form_class = AddElementsForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.is_ajax() and request.user.researcher.can_edit(self.object):
            return super(
                GetItemsToAdd,
                self
            ).get(request, *args, **kwargs)
        return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(
            GetItemsToAdd,
            self
        ).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.add_elements(self.object)
        return super(GetItemsToAdd, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(GetItemsToAdd, self).get_form_kwargs()
        kwargs['selected_project'] = self.object
        kwargs['researcher'] = self.request.user.researcher
        return kwargs

    def get_success_url(self):
        return reverse('project', kwargs={'project_uid': self.object.unique_id})


class GetProtocolsToAdd(GetItemsToAdd):
    template_name = 'protocols_to_add.html'
    initial = {
        'element_type': 'p'
    }


class GetSourcesToAdd(GetItemsToAdd):
    template_name = 'sources_to_add.html'
    initial = {
        'element_type': 's'
    }
