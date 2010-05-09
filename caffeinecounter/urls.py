from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)

# counter patterns
urlpatterns += patterns('caffeinecounter.counter.views',
    url(r'^$', 'index', name='counter-home'),
    url(r'^history/$', 'history', name='counter-history'),
    url(r'^update/$', 'update', name='counter-update'),
)

# direct template rendering
urlpatterns += patterns('django.views.generic.simple',
    url(r'^about/$', 'direct_to_template', {'template': 'counter/about.html'}, name='counter-about'),
)
