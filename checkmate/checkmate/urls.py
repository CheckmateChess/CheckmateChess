from django.conf.urls import patterns, include, url

from django.contrib import admin
from checkmateclient.views import home,start,connect, play

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'checkmate.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
    url(r'^start', start),
    url(r'^connect', connect),
    url(r'^play', play),
)
