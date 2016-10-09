from django.shortcuts import render

from projects.models import Project, Role


def projects_list(request):
    projects_list = Project.objects.filter(roles__user=request.user)
    return render(request, 'projects_list.html', locals())
