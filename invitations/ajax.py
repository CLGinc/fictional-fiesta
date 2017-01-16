from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from .forms import CreateInvitationForm, CreateInvitationModelForm


@login_required
def create_invitation(request):
    if request.is_ajax() and request.method == 'POST':
        form = CreateInvitationForm(
            request.POST or None,
            inviter=request.user.researcher
        )
        if form.is_valid():
            data = data = {
                'email': form.cleaned_data.get('email'),
                'inviter': request.user.researcher.id,
            }
            if form.cleaned_data.get('invitation_object') == 'project':
                data['project'] = form.cleaned_data.get('object_choice').id
            elif form.cleaned_data.get('invitation_object') == 'protocol':
                data['protocol'] = form.cleaned_data.get('object_choice').id
            model_form = CreateInvitationModelForm(data)
            if model_form.is_valid():
                model_form.save()
                return render(
                    request,
                    'invitation_result.html',
                    status=200
                )
        return render(
                request,
                'invitation_result.html',
                status=400
            )
    else:
        return HttpResponseForbidden()
