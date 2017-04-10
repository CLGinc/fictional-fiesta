from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView
from django.views import View
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator


from researchers.models import Role
from researchers.views import RoleListMixin
from .forms import BasicProjectForm
from .models import Project


class SingleProjectMixin(SingleObjectMixin):
    slug_field = 'unique_id'
    slug_url_kwarg = 'project_uid'

    def get_queryset(self):
        return Project.objects.filter(
            roles__researcher=self.request.user.researcher
        )


@method_decorator(login_required, name='dispatch')
class CreateProject(View):
    template_name = 'project_create.html'

    def post(self, request, *args, **kwargs):
        new_project_form = BasicProjectForm(
            request.POST or None,
            researcher=request.user.researcher)
        if new_project_form.is_valid():
            new_project = new_project_form.save()
            return redirect(
                reverse(
                    'project',
                    kwargs={'project_uid': new_project.unique_id}
                )
            )


@method_decorator(login_required, name='dispatch')
class EditProject(UpdateView, SingleProjectMixin):
    context_object_name = 'selected_project'
    template_name = 'project_edit.html'
    form_class = BasicProjectForm

    def get_success_url(self):
        return reverse(
            'project',
            kwargs={'project_uid': self.object.unique_id}
        )


@method_decorator(login_required, name='dispatch')
class ProjectList(ListView, RoleListMixin):
    context_object_name = 'roles_list_page'
    template_name = 'projects_list.html'
    scope = 'project'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.template_name = 'projects_list_page.html'
        return super(ProjectList, self).get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ProjectView(DetailView, SingleProjectMixin):
    context_object_name = 'selected_project'
    template_name = 'project.html'
    form_class = BasicProjectForm

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['can_edit'] = self.request.user.researcher.can_edit(
            self.object
        )
        context['invitation_roles'] = Role.ROLES_TO_INVITE
        context['default_invitation_role'] = Role.DEFAULT_INVITATION_ROLE
        context['participants_by_role'] = \
            self.object.get_participants_by_role()
        return context

    def get_success_url(self):
        return reverse(
            'project',
            kwargs={'project_uid': self.object.unique_id}
        )
