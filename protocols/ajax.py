from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView
from django.http import HttpResponseForbidden, JsonResponse

from .views import SinglePrototolMixin
from users.models import Role
from .models import Protocol


@method_decorator(login_required, name='dispatch')
class ArchiveProtocol(DeleteView, SinglePrototolMixin):
    context_object_name = 'selected_protocol'
    template_name = 'archive_protocol.html'
    http_method_names = [u'post']

    def get_queryset(self):
        return Protocol.objects.filter(
            archived=False,
            roles__role__in=Role.ROLES_CAN_EDIT,
            roles__user=self.request.user
        )

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            self.object = self.get_object()
            return super(
                ArchiveProtocol,
                self
            ).post(request, *args, **kwargs)
        return HttpResponseForbidden()

    def delete(self, request, *args, **kwargs):
        '''
        Calls the archive() method on the fetched object and then
        renders success template.
        '''
        self.template_name = 'archive_protocol_success.html'
        self.object = self.get_object()
        self.object.archive()
        return JsonResponse(
            data=dict(),
            status=200
        )
