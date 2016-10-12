from django.shortcuts import render

from projects.models import Project, Role


def projects_list(request):
    projects_list = request.user.researcher.get_projects_by_roles(
        ['owner', 'contributor', 'watcher'])
    return render(request, 'projects_list.html', locals())
