from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, JsonResponse
from django.views.generic.edit import FormView
from django.views.generic import DeleteView


from users.models import Role
from .views import SingleProjectMixin
from .forms import AddElementsForm
from .models import Project


@method_decorator(login_required, name='dispatch')
class AddItems(FormView, SingleProjectMixin):
    form_class = AddElementsForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.is_ajax() and request.user.can_add_items(self.object):
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
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('projects:project', kwargs={'project_uuid': self.object.uuid})


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


@method_decorator(login_required, name='dispatch')
class ArchiveProject(DeleteView, SingleProjectMixin):
    context_object_name = 'selected_project'
    http_method_names = [u'post']

    def get_queryset(self):
        return Project.objects.filter(
            archived=False,
            roles__role__in=Role.ROLES_CAN_EDIT,
            roles__user=self.request.user
        )

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            self.object = self.get_object()
            return super(
                ArchiveProject,
                self
            ).post(request, *args, **kwargs)
        return HttpResponseForbidden()

    def delete(self, request, *args, **kwargs):
        '''
        Calls the archive() method on the fetched object and then
        renders success template.
        '''
        self.template_name = 'archive_project_success.html'
        self.object = self.get_object()
        self.object.archive()
        return JsonResponse(
            data=dict(),
            status=200
        )
