from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from django.views.generic import DetailView
from django.forms.models import inlineformset_factory

from researchers.views import RoleListMixin
from .models import Protocol, Procedure, Step
from .forms import BasicProtocolForm


class SinglePrototolMixin(SingleObjectMixin):
    slug_field = 'unique_id'
    slug_url_kwarg = 'protocol_uid'

    def get_queryset(self):
        return Protocol.objects.filter(
            roles__researcher=self.request.user.researcher
        )


@method_decorator(login_required, name='dispatch')
class CreateProtocol(FormView):
    template_name = 'protocol_create.html'
    form_class = BasicProtocolForm

    def form_valid(self, form):
        instance = form.save()
        StepsFormset = inlineformset_factory(
            Procedure,
            Step,
            fields=('text',)
        )
        self.steps_formset = StepsFormset(
            self.request.POST,
            instance=instance.procedure
        )
        return super(CreateProtocol, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateProtocol, self).get_context_data(**kwargs)
        StepsFormset = inlineformset_factory(
            Procedure,
            Step,
            fields=('text',)
        )
        context['steps_formset'] = StepsFormset()
        return context

    def get_form_kwargs(self):
        kwargs = super(CreateProtocol, self).get_form_kwargs()
        kwargs['researcher'] = self.request.user.researcher
        return kwargs

    def get_success_url(self):
        return reverse(
            'protocol',
            kwargs={'protocol_uid': self.object.unique_id}
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

    def get_success_url(self):
        self.object = self.get_object()
        return reverse(
            'protocol',
            kwargs={'protocol_uid': self.object.unique_id}
        )
