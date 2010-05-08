from django.http import HttpResponse
from django.views.generic.simple import direct_to_template

def index(request):
    count = 1
    return direct_to_template(request, 'counter/index.html', locals())

def add(request):
    count = 1
    return direct_to_template(request, 'counter/index.html', locals())

def history(request):
    data = ['foo']
    return direct_to_template(request, 'counter/history.html', locals())
