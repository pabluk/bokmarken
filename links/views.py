from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from links.models import Link


def index(request):
    links = Link.objects.all()
    if request.user.is_authenticated():
        links = links.filter(user=request.user).order_by('-id')
    else:
        links = links.filter(is_public=True).order_by('?')
    colors = ['#66D596', '#66A7D5', '#FF566A']

    context = {'links': links, 'colors': colors}
    return render(request, 'links/index.html', context)


def public(request, username):
    public_user = get_object_or_404(User, username=username)
    links = Link.objects.filter(user=public_user, is_public=True).order_by('-id')

    colors = ['#66D596', '#66A7D5', '#FF566A']
    context = {'public_user': public_user, 'links': links, 'colors': colors}
    return render(request, 'links/public.html', context)


@login_required
@ensure_csrf_cookie
def add(request):
    return render(request, 'links/add.html')
