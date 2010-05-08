from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'caffeinecounter.counter.views.index'),
    (r'^add/$', 'caffeinecounter.counter.views.add'),
    (r'^history/$', 'caffeinecounter.counter.views.history'),

    (r'^admin/', include(admin.site.urls)),
)
