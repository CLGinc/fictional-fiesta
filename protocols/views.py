from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView, UpdateView, CreateView
from django.http import Http404

from users.views import RoleListMixin
from users.models import Role
from .models import Protocol, Result
from .forms import BasicProtocolForm
from .forms import BasicResultForm


class SinglePrototolMixin(SingleObjectMixin):
    slug_field = 'uuid'
    slug_url_kwarg = 'protocol_uuid'

    def get_queryset(self):
        return Protocol.objects.filter(
            roles__user=self.request.user
        )


class SinglePrototolResultMixin(SingleObjectMixin):
    slug_field = 'uuid'
    slug_url_kwarg = 'result_uuid'

    def get_queryset(self):
        try:
            selected_protocol = Protocol.objects.get(
                uuid=self.kwargs['protocol_uuid'],
                roles__user=self.request.user
            )
        except Protocol.DoesNotExist:
            selected_protocol = None
        return Result.objects.filter(
            protocol=selected_protocol
        )


@method_decorator(login_required, name='dispatch')
class CreateProtocol(CreateView):
    template_name = 'create_protocol.html'
    form_class = BasicProtocolForm

    def get_success_url(self):
        return reverse(
            'protocols:protocol',
            kwargs={'protocol_uuid': self.object.uuid}
        )

    def get_form_kwargs(self):
        kwargs = super(CreateProtocol, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if 'data' in kwargs:
            kwargs['data'] = kwargs['data'].copy()
            kwargs['data']['last_modified_by'] = str(self.request.user.pk)
        return kwargs


@method_decorator(login_required, name='dispatch')
class UpdateProtocol(UpdateView, SinglePrototolMixin):
    context_object_name = 'selected_protocol'
    template_name = 'update_protocol.html'
    form_class = BasicProtocolForm

    def get_success_url(self):
        return reverse(
            'protocols:protocol',
            kwargs={'protocol_uuid': self.object.uuid}
        )

    def get_form_kwargs(self):
        kwargs = super(UpdateProtocol, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if 'data' in kwargs:
            kwargs['data'] = kwargs['data'].copy()
            kwargs['data']['last_modified_by'] = str(self.request.user.pk)
        return kwargs

    def get_queryset(self):
        return Protocol.objects.filter(
            roles__role__in=Role.ROLES_CAN_EDIT,
            roles__user=self.request.user
        )


@method_decorator(login_required, name='dispatch')
class ProtocoltList(ListView, RoleListMixin):
    context_object_name = 'roles_list_page'
    template_name = 'protocol_list.html'
    scope = 'protocol'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.template_name = 'protocol_list_page.html'
        return super(ProtocoltList, self).get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ProtocolView(DetailView, SinglePrototolMixin):
    context_object_name = 'selected_protocol'
    template_name = 'protocol.html'

    def get_context_data(self, **kwargs):
        context = super(ProtocolView, self).get_context_data(**kwargs)
        context['role'] = self.object.roles.get(user=self.request.user)
        context['can_update'] = self.request.user.can_update(
            self.object
        )
        context['can_add_items'] = self.request.user.can_add_items(
            self.object
        )
        context['invitation_roles'] = Role.ROLES_TO_INVITE
        context['assets_by_category'] = self.object.get_assets_by_category()
        context['participants_by_role'] = \
            self.object.get_participants_by_role()
        return context


@method_decorator(login_required, name='dispatch')
class CreateProtocolResult(CreateView):
    template_name = 'create_protocol_result.html'
    form_class = BasicResultForm
    protocol_slug_field = 'uuid'
    protocol_slug_url_kwarg = 'protocol_uuid'

    def get(self, request, *args, **kwargs):
        self.protocol = self.get_protocol()
        return super(CreateProtocolResult, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.protocol = self.get_protocol()
        return super(CreateProtocolResult, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'protocols:protocol_result',
            kwargs={
                'protocol_uuid': self.object.protocol.uuid,
                'result_uuid': self.object.uuid,
            }
        )

    def get_context_data(self, **kwargs):
        context = dict()
        context['selected_protocol'] = self.protocol
        context.update(
            super(CreateProtocolResult, self).get_context_data(**kwargs)
        )
        return context

    def get_protocol_queryset(self):
        return Protocol.objects.filter(
            roles__user=self.request.user
        )

    def get_protocol(self, queryset=None):
        if queryset is None:
            queryset = self.get_protocol_queryset()
        slug = self.kwargs.get(self.protocol_slug_url_kwarg)
        if slug is not None:
            slug_field = self.protocol_slug_field
            queryset = queryset.filter(**{slug_field: slug})

        try:
            protocol = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                ("No %(verbose_name)s found matching the query") %
                {'verbose_name': queryset.model._meta.verbose_name}
            )
        return protocol

    def get_form_kwargs(self):
        kwargs = super(CreateProtocolResult, self).get_form_kwargs()
        if 'data' in kwargs:
            kwargs['data'] = kwargs['data'].copy()
            kwargs['data']['owner'] = str(self.request.user.pk)
        kwargs['protocol'] = self.protocol
        kwargs['user'] = self.request.user
        return kwargs


@method_decorator(login_required, name='dispatch')
class UpdateProtocolResult(UpdateView, SinglePrototolResultMixin):
    context_object_name = 'selected_protocol_result'
    form_class = BasicResultForm
    template_name = 'update_protocol_result.html'

    def get_success_url(self):
        return reverse(
            'protocols:protocol_result',
            kwargs={
                'protocol_uuid': self.object.protocol.uuid,
                'result_uuid': self.object.uuid,
            }
        )

    def get_form_kwargs(self):
        kwargs = super(UpdateProtocolResult, self).get_form_kwargs()
        if 'data' in kwargs:
            kwargs['data'] = kwargs['data'].copy()
            kwargs['data']['owner'] = str(self.request.user.pk)
        kwargs['protocol'] = self.object.protocol
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        queryset = super(UpdateProtocolResult, self).get_queryset()
        return queryset.filter(owner=self.request.user)


@method_decorator(login_required, name='dispatch')
class ProtocolResultView(DetailView, SinglePrototolResultMixin):
    context_object_name = 'selected_protocol_result'
    template_name = 'protocol_result.html'
