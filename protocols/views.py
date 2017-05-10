from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView, UpdateView, CreateView
from django.http import Http404

from researchers.views import RoleListMixin
from researchers.models import Role
from .models import Protocol, Result
from .forms import BasicProtocolForm, StepsFormset
from .forms import BasicResultForm, DataColumnsFormset


class SinglePrototolMixin(SingleObjectMixin):
    slug_field = 'unique_id'
    slug_url_kwarg = 'protocol_uid'

    def get_queryset(self):
        return Protocol.objects.filter(
            roles__researcher=self.request.user.researcher
        )


class SinglePrototolResultMixin(SingleObjectMixin):
    slug_field = 'unique_id'
    slug_url_kwarg = 'result_uid'

    def get_queryset(self):
        try:
            selected_protocol = Protocol.objects.get(
                unique_id=self.kwargs['protocol_uid'],
                roles__researcher=self.request.user.researcher
            )
        except Protocol.DoesNotExist:
            selected_protocol = None
        return Result.objects.filter(
            protocol=selected_protocol
        )


@method_decorator(login_required, name='dispatch')
class CreateViewWithFormset(CreateView):
    formset_class = None
    formset_name = ''

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_class(request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object.procedure
        formset.save()
        return super(CreateViewWithFormset, self).form_valid(form)

    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


    def get_context_data(self, **kwargs):
        context = dict()
        context[self.formset_name] = self.formset_class()
        context.update(super(CreateViewWithFormset, self).get_context_data(**kwargs))
        return context


@method_decorator(login_required, name='dispatch')
class UpdateViewWithFormset(UpdateView):
    formset_class = None
    formset_name = ''
    formset_instance = None

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_class(
            instance=self.object.procedure,
            data=request.POST
        )
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        formset.save()
        return super(UpdateViewWithFormset, self).form_valid(form)

    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


    def get_context_data(self, **kwargs):
        context = dict()
        context[self.formset_name] = self.formset_class(instance=self.formset_instance)
        context.update(super(UpdateViewWithFormset, self).get_context_data(**kwargs))
        return context


@method_decorator(login_required, name='dispatch')
class CreateProtocol(CreateViewWithFormset):
    template_name = 'protocol_create.html'
    form_class = BasicProtocolForm
    formset_class = StepsFormset
    formset_name = 'steps_formset'

    def get_success_url(self):
        return reverse(
            'protocol',
            kwargs={'protocol_uid': self.object.unique_id}
        )

    def get_form_kwargs(self):
        kwargs = super(CreateProtocol, self).get_form_kwargs()
        kwargs['researcher'] = self.request.user.researcher
        return kwargs


@method_decorator(login_required, name='dispatch')
class UpdateProtocol(UpdateViewWithFormset, SinglePrototolMixin):
    context_object_name = 'selected_protocol'
    template_name = 'protocol_edit.html'
    form_class = BasicProtocolForm
    formset_class = StepsFormset
    formset_name = 'steps_formset'
    formset_instance = None

    def get_success_url(self):
        return reverse(
            'protocol',
            kwargs={'protocol_uid': self.object.unique_id}
        )

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        self.formset_instance = self.get_formset_instance()
        return super(UpdateProtocol, self).get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(UpdateProtocol, self).get_form_kwargs()
        kwargs['researcher'] = self.request.user.researcher
        return kwargs

    def get_formset_instance(self):
        return self.object.procedure


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
        context['can_edit'] = self.request.user.researcher.can_edit(
            self.object
        )
        context['invitation_roles'] = Role.ROLES_TO_INVITE
        context['assets_by_category'] = self.object.get_assets_by_category()
        context['participants_by_role'] = \
            self.object.get_participants_by_role()
        return context


@method_decorator(login_required, name='dispatch')
class CreateProtocolResult(CreateViewWithFormset, SinglePrototolMixin):
    template_name = 'protocol_create_result.html'
    form_class = BasicResultForm
    slug_field = 'unique_id'
    slug_url_kwarg = 'protocol_uid'
    formset_class = DataColumnsFormset
    formset_name = 'data_columns_formset'

    def get(self, request, *args, **kwargs):
        return super(CreateProtocolResult, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(CreateProtocolResult, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'protocol_result',
            kwargs={
                'protocol_uid': self.object.protocol.unique_id,
                'result_uid': self.object.unique_id,
            }
        )

    def get_context_data(self, **kwargs):
        self.protocol = self.get_protocol()
        context = dict()
        context['selected_protocol'] = self.get_protocol()
        context.update(
            super(CreateProtocolResult, self).get_context_data(**kwargs)
        )
        return context

    def get_protocol(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        try:
            protocol = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                ("No %(verbose_name)s found matching the query") %
                {'verbose_name': queryset.model._meta.verbose_name}
            )
        return protocol


@method_decorator(login_required, name='dispatch')
class UpdateProtocolResult(UpdateViewWithFormset, SinglePrototolResultMixin):
    context_object_name = 'selected_protocol_result'
    template_name = 'protocol_result_edit.html'
    form_class = BasicResultForm
    formset_class = DataColumnsFormset
    formset_name = 'data_columns_formset'
    formset_instance = None

    def get_success_url(self):
        return reverse(
            'protocol_result',
            kwargs={
                'protocol_uid': self.object.protocol.unique_id,
                'result_uid': self.object.unique_id,
            }
        )

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        self.formset_instance = self.get_formset_instance()
        return super(UpdateProtocol, self).get_context_data(**kwargs)

    def get_formset_instance(self):
        return self.object


@method_decorator(login_required, name='dispatch')
class ProtocolResultView(DetailView, SinglePrototolResultMixin):
    context_object_name = 'selected_protocol_result'
    template_name = 'protocol_result.html'

    def get_context_data(self, **kwargs):
        context = super(ProtocolResultView, self).get_context_data(**kwargs)
        return context
