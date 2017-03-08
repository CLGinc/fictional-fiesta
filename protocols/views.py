from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from researchers.views import RoleListMixin


@method_decorator(login_required, name='dispatch')
class ProtocoltList(ListView, RoleListMixin):
    context_object_name = 'roles_list_page'
    template_name = 'protocol_list.html'
    scope = 'protocol'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.template_name = 'protocol_list.html'
        return super(ProtocoltList, self).get(request, *args, **kwargs)
