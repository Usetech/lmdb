import os
from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lanit_mdb.views.home', name='home'),
    # url(r'^lanit_mdb/', include('lanit_mdb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^favicon.ico$', 'django.views.static.serve', {'path': 'favicon.ico', 'document_root': settings.STATIC_ROOT}),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^selectable/', include('selectable.urls')),
    url(r'^legalentity/(?P<id>\d+)/$', 'core.views.legal_entity', name='legal_entity'),
    url(r'', include(admin.site.urls)),
)
