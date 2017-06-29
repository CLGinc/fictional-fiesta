from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView
from django.views.generic import ListView, DetailView, CreateView
from django.utils.decorators import method_decorator


from users.models import Role
from users.views import RoleListMixin
from .forms import BasicProjectForm
from .models import Project


class SingleProjectMixin(SingleObjectMixin):
    slug_field = 'uuid'
    slug_url_kwarg = 'project_uuid'

    def get_queryset(self):
        return Project.objects.filter(
            roles__user=self.request.user
        )


@method_decorator(login_required, name='dispatch')
class CreateProject(CreateView):
    template_name = 'create_project.html'
    form_class = BasicProjectForm

    def get_form_kwargs(self):
        kwargs = super(CreateProject, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse(
            'project',
            kwargs={'project_uuid': self.object.uuid}
        )


@method_decorator(login_required, name='dispatch')
class UpdateProject(UpdateView, SingleProjectMixin):
    context_object_name = 'selected_project'
    template_name = 'update_project.html'
    form_class = BasicProjectForm

    def get_success_url(self):
        return reverse(
            'project',
            kwargs={'project_uuid': self.object.uuid}
        )

    def get_queryset(self):
        return Project.objects.filter(
            roles__role__in=Role.ROLES_CAN_EDIT,
            roles__user=self.request.user
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
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['role'] = self.object.roles.get(user=self.request.user)
        context['can_update'] = self.request.user.can_update(
            self.object
        )
        context['can_add_items'] = self.request.user.can_add_items(
            self.object
        )
        context['invitation_roles'] = Role.ROLES_TO_INVITE
        context['default_invitation_role'] = Role.DEFAULT_INVITATION_ROLE
        context['participants_by_role'] = \
            self.object.get_participants_by_role()
        protocols_with_permission = [(x, x.has_role(self.request.user)) for x in self.object.protocols.all()]
        context['protocols_with_permission'] = protocols_with_permission
        results_with_permission = [(x, x.protocol.has_role(self.request.user)) for x in self.object.results.all()]
        context['results_with_permission'] = results_with_permission
        return context

    def get_success_url(self):
        return reverse(
            'project',
            kwargs={'project_uuid': self.object.uuid}
        )
