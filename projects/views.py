from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Role


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
        roles_list = roles_list.filter(project__name__contains=request.GET.get('name'))
    paginator = Paginator(roles_list, 15)
    page = request.GET.get('page')
    try:
        roles_list_page = paginator.page(page)
    except PageNotAnInteger:
        roles_list_page = paginator.page(number=1)
    except EmptyPage:
        roles_list_page = paginator.page(paginator.num_pages)
    return render(request, 'projects_list.html', locals())
