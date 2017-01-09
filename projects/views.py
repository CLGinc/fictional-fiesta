from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import FieldError
from django.template.context_processors import csrf
from django.http import HttpResponseBadRequest
from django.template.response import TemplateResponse

from researchers.models import Role
from researchers.forms import ProjectRolesListForm
from .forms import NewProjectForm, AddElementsForm
from .models import Project


@login_required
def projects_list(request):
    # Handle new project creation
    if request.method == 'POST':
        new_project_form = NewProjectForm(request.POST or None)
        if new_project_form.is_valid():
            new_project = new_project_form.save(
                researcher=request.user.researcher)
            return redirect('/projects/{}'.format(new_project.unique_id))
    elif request.method == 'GET':
        roles_labels = Role.ROLES
        form = ProjectRolesListForm(request.GET, researcher=request.user.researcher)
        if form.is_valid():
            roles_list = form.project_roles
        paginator = Paginator(roles_list, 15)
        roles_list_page = paginator.page(1)
        if request.is_ajax():
            page = request.GET.get('page')
            try:
                roles_list_page = paginator.page(page)
            except PageNotAnInteger:
                return HttpResponseBadRequest(reason='Page must be integer!')
            except EmptyPage:
                return HttpResponseBadRequest(reason='Page does not exist!')
            return render(request, 'projects_list_page.html', locals())
        try:
            return render(request, 'projects_list.html', locals())
        except FieldError:
            return HttpResponseBadRequest('Parameter order_by not valid!')


@login_required
def project(request, project_uid):
    selected_project = get_object_or_404(Project, unique_id=project_uid)
    researcher = request.user.researcher
    can_edit = researcher.can_edit(selected_project)

    if request.method == 'GET':
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
        if request.POST.get('element_type') == 'p':
            protocols_to_add = researcher.protocols_to_add(selected_project)
            add_elements_form = AddElementsForm(
                request.POST or None,
                queryset=protocols_to_add)
        elif request.POST.get('element_type') == 's':
            sources_to_add = researcher.sources.all().exclude(
                id__in=[o.id for o in selected_project.sources.all()])
            add_elements_form = AddElementsForm(
                request.POST or None,
                queryset=sources_to_add)
        if add_elements_form.is_valid():
            element_type = add_elements_form.cleaned_data['element_type']
            if element_type == 'p':
                selected_project.protocols.add(
                    *list(add_elements_form.cleaned_data['element_choices']))
            elif element_type == 's':
                selected_project.sources.add(
                    *list(add_elements_form.cleaned_data['element_choices']))
        return redirect('.')
    else:
        return HttpResponseBadRequest('Method not supported!')
