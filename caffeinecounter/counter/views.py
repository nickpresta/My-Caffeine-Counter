from django.http import HttpResponse
from django.views.generic.simple import direct_to_template

from caffeinecounter.counter.models import *

from datetime import datetime
from collections import defaultdict
import operator


def index(request):
    try:
        count = Counter.objects.get(date__range=(datetime.now(), datetime.now())).count
    except Counter.DoesNotExist:
        Counter(count=0).save()
        count = 0

    d = defaultdict(int)
    for item in Countable.objects.all():
        d[item.type.name] += 1
    common_choice = max(d.iteritems(), key=operator.itemgetter(1))[0]
    return direct_to_template(request, 'counter/index.html', locals())

def update(request):
    if 'n' in request.GET and request.GET['n'].strip() and 'type' in request.GET and request.GET['type'].strip():
        if request.is_ajax():
            # update count here
            try:
                c = Counter.objects.get(date__range=(datetime.now(), datetime.now()))
                try:
                    t = Type.objects.get(name__iexact=request.GET['type'].strip())
                except:
                    # create on the fly
                    t = Type(name=request.GET['type'])
                    t.save()

                Countable(type=t, counter=c).save()
                c.count += 1
                c.save()
            except Counter.DoesNotExist:
                Counter(count=0).save()
                return HttpResponse("0")


            d = defaultdict(int)
            for item in Countable.objects.all():
                d[item.type.name] += 1
            common_choice = max(d.iteritems(), key=operator.itemgetter(1))[0]
            return HttpResponse("%s,%s" % ((int(request.GET['n']) + 1), common_choice))

    return HttpResponse("Missing required GET parameters")

def history(request):
    data = ['foo']
    return direct_to_template(request, 'counter/history.html', locals())
