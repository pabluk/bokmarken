from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from links.models import Link
from links.forms import LinkForm


def index(request):
    if request.user.is_authenticated():
        return redirect('links', username=request.user.username)
    links = Link.objects.filter(is_public=True).order_by('?')
    colors = ['#66D596', '#66A7D5', '#FF566A']
    context = {'links': links, 'colors': colors}
    return render(request, 'links/index.html', context)


def links(request, username):
    user = get_object_or_404(User, username=username)
    links = Link.objects.filter(user=user)
    colors = ['#66D596', '#66A7D5', '#FF566A']
    context = {'links': links, 'colors': colors}
    return render(request, 'links/links.html', context)


@login_required
def add(request, username=''):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()
            return redirect('links', username=request.user.username)
    else:
        form = LinkForm()

    context = {'form': form}
    return render(request, 'links/add.html', context)
