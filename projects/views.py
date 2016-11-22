from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.context_processors import csrf
from django.http import Http404

from researchers.models import Role
from .forms import NewProjectForm
from .models import Project


def projects_list(request):
    roles_labels = Role.ROLES
    selected_roles = request.GET.getlist('role')
    if request.GET.getlist('role'):
        roles_list = request.user.researcher.get_roles(
            scope='project',
            roles=selected_roles)
    else:
        roles_list = request.user.researcher.get_roles(scope='project')
    if request.GET.get('name'):
        name_filter = request.GET.get('name')
        roles_list = roles_list.filter(
            project__name__icontains=request.GET.get('name'))

    new_project_form = NewProjectForm(request.POST or None)
    if request.method == 'POST':
        if new_project_form.is_valid():
            new_project_form.save()
            new_project_role = Role.objects.create(
                researcher=request.user.researcher,
                project=new_project_form.instance,
                role='owner')
            new_project_role.save()
            return redirect(
                '/projects/{}'.format(new_project_form.instance.unique_id))
    paginator = Paginator(roles_list, 15)
    page = request.GET.get('page')
    try:
        roles_list_page = paginator.page(page)
    except PageNotAnInteger:
        roles_list_page = paginator.page(number=1)
    except EmptyPage:
        roles_list_page = paginator.page(paginator.num_pages)
    return render(request, 'projects_list.html', locals())


def project(request, project_id):
    try:
        selected_project = Project.objects.get(unique_id=project_id)
    except Project.DoesNotExist:
        raise Http404()
    return render(request, 'project.html', locals())
