from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web.views.home', name='home'),
    url(r'^add/$', 'web.views.add', name='add'),
    url(r'^show/(?P<uuid>[0-9a-f\-]+)/$', 'web.views.show', name='show'),
    # url(r'^seamless/', include('seamless.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
)
