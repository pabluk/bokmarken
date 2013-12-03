from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from links.models import Linkshelf
from links.forms import LinkForm


def linkshelf(request, name):
    linkshelf = get_object_or_404(Linkshelf, name=name)
    colors = ['#66D596', '#66A7D5', '#FF566A']
    context = {'linkshelf': linkshelf, 'colors': colors}
    return render(request, 'links/linkshelf.html', context)


@login_required
def add(request):
    linkshelf = request.user.linkshelf_set.latest('id')
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.linkshelf = linkshelf
            link.save()
            return redirect('index')
    else:
        form = LinkForm()

    context = {'form': form}
    return render(request, 'links/add.html', context)
