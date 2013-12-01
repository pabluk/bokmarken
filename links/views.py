from django.shortcuts import render

from links.models import Linkshelf


def index(request):
    linkshelf = Linkshelf.objects.latest('id')
    colors = ['#66D596', '#66A7D5', '#FF566A']
    context = {'linkshelf': linkshelf, 'colors': colors}
    return render(request, 'links/index.html', context)
