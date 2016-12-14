from datetime import datetime

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import FieldError
from django.template.context_processors import csrf
from django.http import Http404, HttpResponseBadRequest
from django.template.response import TemplateResponse

from researchers.models import Role
from .forms import NewProjectForm
from .models import Project


def projects_list(request):
    # Handle new project creation
    if request.method == 'POST':
        new_project_form = NewProjectForm(request.POST or None)
        if new_project_form.is_valid():
            new_project_form.save()
            new_project_role = Role.objects.create(
                researcher=request.user.researcher,
                project=new_project_form.instance,
                role='owner')
            new_project_role.save()
            return redirect(
                '/projects/{}'.format(new_project_form.instance.unique_id))
    elif request.method == 'GET':
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
        if request.GET.get('created-from'):
            created_from = datetime.strptime(
                request.GET.get('created-from'),
                '%Y-%m-%d').date()
            roles_list = roles_list.filter(
                project__datetime_created__date__gte=created_from)
        if request.GET.get('created-to'):
            created_to = datetime.strptime(
                request.GET.get('created-to'),
                '%Y-%m-%d').date()
            roles_list = roles_list.filter(
                project__datetime_created__date__lte=created_to)
        if request.GET.get('order-by'):
            order_by = request.GET.get('order-by')
            roles_list = roles_list.order_by(order_by)
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
        try:
            return render(request, 'projects_list.html', locals())
        except FieldError:
            return HttpResponseBadRequest('Parameter order_by not valid!')


def project(request, project_id):
    if request.method == 'GET':
        try:
            selected_project = Project.objects.get(unique_id=project_id)
            if request.is_ajax():
                if request.GET.get('protocols_to_add_list'):
                    protocols_roles_to_add = request.user.researcher.get_roles(
                        scope='protocol',
                        roles=('owner', 'contributor')
                        ).exclude(
                            protocol__in=selected_project.protocols.all())
                    return render(
                        request,
                        'protocols_to_add.html',
                        locals())
                elif request.GET.get('sources_to_add_list'):
                    sources_to_add = request.user.researcher.sources.all()
                    return render(
                        request,
                        'sources_to_add.html',
                        locals()
                    )
            results = selected_project.results.all()
            participants_by_role = selected_project.get_participants_by_role()
            paginator = Paginator(results, 15)
            results_page = paginator.page(1)
            # hangle ajax pagination
            if request.is_ajax():
                page = request.GET.get('page')
                try:
                    results_page = paginator.page(page)
                except PageNotAnInteger:
                    return HttpResponseBadRequest(reason='Page must be integer!')
                except EmptyPage:
                    return HttpResponseBadRequest(reason='Page does not exist!')

        except Project.DoesNotExist:
            raise Http404()
        return render(request, 'project.html', locals())
