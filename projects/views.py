from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.context_processors import csrf

from .models import Role
from .forms import NewProjectForm


def projects_list(request):
    is_filtered = False
    roles_labels = Role.ROLES
    selected_roles = request.GET.getlist('role')
    if request.GET.getlist('role'):
        roles_list = request.user.researcher.get_roles(
            scope='project',
            roles=selected_roles)
        is_filtered = True
    else:
        roles_list = request.user.researcher.get_roles(scope='project')
    if request.GET.get('name'):
        name_filter = request.GET.get('name')
        roles_list = roles_list.filter(project__name__icontains=request.GET.get('name'))
        is_filtered = True

    new_project_form = NewProjectForm(request.POST or None)
    if request.method == 'POST':
        if new_project_form.is_valid():
            new_project_form.save()
            new_project_role = Role.objects.create(user=request.user, project=new_project_form.instance, role='owner')
            new_project_role.save()
            return redirect('/projects/')
    paginator = Paginator(roles_list, 15)
    page = request.GET.get('page')
    try:
        roles_list_page = paginator.page(page)
    except PageNotAnInteger:
        roles_list_page = paginator.page(number=1)
    except EmptyPage:
        roles_list_page = paginator.page(paginator.num_pages)
    return render(request, 'projects_list.html', locals())
