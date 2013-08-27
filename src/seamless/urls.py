from django.conf.urls import patterns, include, url
from haystack import urls
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web.views.home', name='home'),
    url(r'^add/$', 'web.views.add', name='add'),
    url(r'^show/(?P<uuid>[0-9a-f\-]+)/$', 'web.views.show', name='show'),
    url(r'^edit/(?P<uuid>[0-9a-f\-]+)/auth/(?P<auth_code>[0-9a-f\-]+)/$', 'web.views.edit', name='edit'),
    url(r'^edit/(?P<uuid>[0-9a-f\-]+)/$', 'web.views.edit_without_auth', name='edit_without_auth'),
    url(r'^rate/(?P<uuid>[0-9a-f\-]+)/(?P<rating>[0-9]{1,2})/$', 'web.views.rate', name='rate'),
    
    url(r'^api/get-by-uniquename/(?P<uniquename>[0-9a-z\-~A-Z_]+)/$', 'api.views.get_by_uniquename', name='get_by_uniquename'),
    url(r'^api/version-info', 'api.views.version_info', name="version_info"),
    
    # url(r'^seamless/', include('seamless.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', include('haystack.urls')),
)
