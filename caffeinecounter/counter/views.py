from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required

from caffeinecounter.counter.models import *
from caffeinecounter.settings import USER

from datetime import datetime
from collections import defaultdict
import operator

# These next 2 lines get rid of a TclError when you don't
# have a $DISPLAY variable set (like on my server)
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.backends.backend_agg import FigureCanvasAgg

def index(request):
    """ Responsible for grabbing the current count, creating today's counter, 
        and the latest addition/most common choice """
    try:
        todays_count = Counter.objects.get(date__range=(datetime.now(), datetime.now()))
        count = todays_count.count
    except Counter.DoesNotExist:
        todays_count = Counter(count=0)
        todays_count.save()
        count = 0

    d = defaultdict(int)
    for item in Countable.objects.all():
        d[item.type.name] += 1

    try:
        common_choice = max(d.iteritems(), key=operator.itemgetter(1))[0]
    except ValueError:
        # No countables yet...
        common_choice = ""

    try:
        latest_addition = Countable.objects.filter(counter=todays_count).order_by('-added')[0]
    except (Countable.DoesNotExist, IndexError):
        latest_addition = ""


    theUser = USER

    return direct_to_template(request, 'counter/index.html', locals())

@login_required
def update(request):
    """ Updates the count and returns the new count and most common data choice """

    if 'n' in request.GET and request.GET['n'].strip() and \
       'type' in request.GET and request.GET['type'].strip():
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

            try:
                common_choice = max(d.iteritems(), key=operator.itemgetter(1))[0]
            except ValueError:
                # No countables yet...
                common_choice = ""

            return HttpResponse("%s,%s" % ((int(request.GET['n']) + 1), common_choice))

    return HttpResponse("FAIL")

def gen_image(request):
    """ This will generate images for inclusion (via <img...>)
        on the history.html page """

    # ADAPTED FROM:
    # http://matplotlib.sourceforge.net/examples/api/barchart_demo.html

    N = 7
    daily = [0] * N

    # generate data from the last week
    all_counts = Counter.objects.all().order_by('-date')[:7]
    for c in all_counts:
        daily[c.date.weekday()] = len(Countable.objects.filter(counter=c))

    ind = np.arange(N)
    width = 0.5

    fig = plt.figure()
    ax = fig.add_subplot(111)
    bars = ax.bar(ind + width / 2.0, daily, width, color='green')

    # Set labels and such 
    ax.set_title("Caffeine Per Day (Last Week)")
    ax.set_ylabel("Daily Amount")
    ax.set_xticks(ind + width)
    ax.set_xticklabels(("Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"))

    # Attach text labels
    for b in bars:
        height = b.get_height()
        ax.text(b.get_x() + b.get_width() / 2.0, 1.05 * height, "%d" % int(height), ha='center', va='bottom')

    canvas = FigureCanvasAgg(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
