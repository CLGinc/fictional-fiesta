from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views import View
from django.views.generic import ListView
from django.utils.decorators import method_decorator


from researchers.models import Role
from researchers.views import RoleListMixin
from .forms import NewProjectForm
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
    def post(self, request, *args, **kwargs):
        new_project_form = NewProjectForm(request.POST or None)
        if new_project_form.is_valid():
            new_project = new_project_form.save(
                researcher=request.user.researcher)
            return redirect(
                reverse(
                    'project',
                    kwargs={'project_uid': new_project.unique_id}
                )
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

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['can_edit'] = self.request.user.researcher.can_edit(
            self.object
        )
        context['invitation_roles'] = Role.ROLES_TO_INVITE
        context['participants_by_role'] = \
            self.object.get_participants_by_role()
        return context
