from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.views.generic.edit import FormView

from .views import SingleProjectMixin
from .forms import AddElementsForm


@method_decorator(login_required, name='dispatch')
class AddItems(FormView, SingleProjectMixin):
    form_class = AddElementsForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.is_ajax() and request.user.researcher.can_edit(self.object):
            return super(
                AddItems,
                self
            ).get(request, *args, **kwargs)
        return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(
            AddItems,
            self
        ).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.add_elements(self.object)
        return super(AddItems, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AddItems, self).get_form_kwargs()
        kwargs['selected_project'] = self.object
        kwargs['researcher'] = self.request.user.researcher
        return kwargs

    def get_success_url(self):
        return reverse('project', kwargs={'project_uid': self.object.unique_id})


@method_decorator(login_required, name='dispatch')
class AddProtocols(AddItems):
    template_name = 'protocols_to_add.html'
    initial = {
        'element_type': 'p'
    }


@method_decorator(login_required, name='dispatch')
class AddSources(AddItems):
    template_name = 'sources_to_add.html'
    initial = {
        'element_type': 's'
    }
