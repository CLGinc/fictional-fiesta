from django.shortcuts import render

from projects.models import Project, Role


def projects_list(request):
    roles_list = request.user.researcher.get_roles(scope='project')
    return render(request, 'projects_list.html', locals())
