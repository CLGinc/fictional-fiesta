from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView, UpdateView, CreateView

from researchers.views import RoleListMixin
from researchers.models import Role
from .models import Protocol, Result
from .forms import BasicProtocolForm, StepsFormset


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
class CreateProtocol(CreateView):
    template_name = 'protocol_create.html'
    form_class = BasicProtocolForm

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        steps_formset = StepsFormset(request.POST)
        if form.is_valid() and steps_formset.is_valid():
            return self.form_valid(form, steps_formset)
        else:
            return self.form_invalid(form, steps_formset)

    def form_valid(self, form, steps_formset):
        self.object = form.save()
        steps_formset.instance = self.object.procedure
        steps_formset.save()
        return super(CreateProtocol, self).form_valid(form)

    def form_invalid(self, form, steps_formset):
        return self.render_to_response(
            self.get_context_data(form=form, steps_formset=steps_formset)
        )

    def get_form_kwargs(self):
        kwargs = super(CreateProtocol, self).get_form_kwargs()
        kwargs['researcher'] = self.request.user.researcher
        return kwargs

    def get_success_url(self):
        return reverse(
            'protocol',
            kwargs={'protocol_uid': self.object.unique_id}
        )

    def get_context_data(self, **kwargs):
        context = dict()
        context['steps_formset'] = StepsFormset()
        context.update(super(CreateProtocol, self).get_context_data(**kwargs))
        return context


@method_decorator(login_required, name='dispatch')
class UpdateProtocol(UpdateView, SinglePrototolMixin):
    context_object_name = 'selected_protocol'
    template_name = 'protocol_edit.html'
    form_class = BasicProtocolForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        steps_formset = StepsFormset(
            instance=self.object.procedure,
            data=request.POST
        )
        if form.is_valid() and steps_formset.is_valid():
            return self.form_valid(form, steps_formset)
        else:
            return self.form_invalid(form, steps_formset)

    def form_valid(self, form, steps_formset):
        steps_formset.save()
        return super(UpdateProtocol, self).form_valid(form)

    def form_invalid(self, form, steps_formset):
        return self.render_to_response(
            self.get_context_data(form=form, steps_formset=steps_formset)
        )

    def get_form_kwargs(self):
        kwargs = super(UpdateProtocol, self).get_form_kwargs()
        kwargs['researcher'] = self.request.user.researcher
        return kwargs

    def get_success_url(self):
        return reverse(
            'protocol',
            kwargs={'protocol_uid': self.object.unique_id}
        )

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = dict()
        context['steps_formset'] = StepsFormset(instance=self.object.procedure)
        context.update(super(UpdateProtocol, self).get_context_data(**kwargs))
        return context


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
class CreateProtocolResult(CreateView):
    template_name = 'protocol_create_result.html'
    model = Result
    fields = ['note']


@method_decorator(login_required, name='dispatch')
class ProtocolResultView(DetailView, SinglePrototolResultMixin):
    context_object_name = 'selected_protocol_result'
    template_name = 'protocol_result.html'

    def get_context_data(self, **kwargs):
        context = super(ProtocolResultView, self).get_context_data(**kwargs)
        return context
