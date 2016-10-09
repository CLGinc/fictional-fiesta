from django.shortcuts import render


def projects_list(request):
    return render(request, 'projects_list.html', locals())
