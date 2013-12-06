from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from links.models import Link
from links.forms import LinkForm


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
    user = get_object_or_404(User, username=username)
    links = Link.objects.filter(user=user, is_public=True).order_by('-id')

    colors = ['#66D596', '#66A7D5', '#FF566A']
    context = {'user': user, 'links': links, 'colors': colors}
    return render(request, 'links/public.html', context)


@login_required
def add(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()
            return redirect('index')
    else:
        form = LinkForm()

    context = {'form': form}
    return render(request, 'links/add.html', context)
