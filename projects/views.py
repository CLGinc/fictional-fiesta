from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from projects.models import Project, Role


def projects_list(request):
    roles_list = request.user.researcher.get_roles(scope='project')
    paginator = Paginator(roles_list, 15)
    page = request.GET.get('page')
    try:
        request_items_page = paginator.page(page)
    except PageNotAnInteger:
        request_items_page = paginator.page(number=1)
    except EmptyPage:
        request_items_page = paginator.page(paginator.num_pages)
    return render(request, 'projects_list.html', locals())
