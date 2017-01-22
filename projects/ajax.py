from django.http import HttpResponseForbidden, HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Project


def get_protocols_to_add(request, project_uid):
    if request.is_ajax() and request.method == 'GET':
        selected_project = get_object_or_404(Project, unique_id=project_uid)
        researcher = request.user.researcher
        protocols_to_add = researcher.get_protocols_to_add(
            selected_project)
        return render(
            request,
            'protocols_to_add.html',
            locals())
    else:
        return HttpResponseForbidden()


def get_sources_to_add(request, project_uid):
    if request.is_ajax() and if request.method == 'GET':
        selected_project = get_object_or_404(Project, unique_id=project_uid)
        researcher = request.user.researcher
        sources_to_add = researcher.get_sources_to_add(selected_project)
        return render(
            request,
            'sources_to_add.html',
            locals()
        )
    else:
        return HttpResponseForbidden()
