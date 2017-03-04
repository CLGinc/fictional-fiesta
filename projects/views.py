from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.views.generic import ListView
from django.utils.decorators import method_decorator


from researchers.models import Role
from researchers.forms import ProjectRolesListForm
from researchers.views import RoleListMixin
from .forms import NewProjectForm, AddElementsForm
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

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.template_name = 'projects_list_page.html'
        return super(ProjectList, self).get(request, *args, **kwargs)


@login_required
def project(request, project_uid):
    selected_project = get_object_or_404(Project, unique_id=project_uid)
    researcher = request.user.researcher
    if not(researcher.can_view(selected_project)):
        return render(request, 'project_cannot_view.html', locals())
    can_edit = researcher.can_edit(selected_project)

    if request.method == 'GET':
        invitation_roles = Role.ROLES_TO_INVITE
        results = selected_project.results.all()
        participants_by_role = selected_project.get_participants_by_role()
        paginator = Paginator(results, 15)
        if request.is_ajax():
            # hangle ajax pagination
            if request.GET.get('page'):
                page = request.GET.get('page')
                try:
                    results_page = paginator.page(page)
                except PageNotAnInteger:
                    return HttpResponseBadRequest(
                        reason='Page must be integer!')
                except EmptyPage:
                    return HttpResponseBadRequest(
                        reason='Page does not exist!')
                return render(request, 'project_results_page.html', locals())
            else:
                return HttpResponseBadRequest(reason='Request not supported!')
        results_page = paginator.page(1)
        return render(request, 'project.html', locals())
    elif request.method == 'POST' and can_edit:
        add_elements_form = AddElementsForm(
            request.POST or None,
            selected_project=selected_project,
            researcher=researcher)
        if add_elements_form.is_valid():
            add_elements_form.add_elements(selected_project)
        return redirect('.')
    else:
        return HttpResponseBadRequest('Method not supported!')
