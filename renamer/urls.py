from django.conf.urls import patterns, include, url, static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = []
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^admin/', include(admin.site.urls))
    )

    urlpatterns += patterns('renamer.views.main',
        url(r'^$', 'home', name="home"),
        url(r'^manage/$', 'manage', name="manage"),
        url(r'^to_archive/$', 'to_archive'),
        url(r'^to_diva/$', 'to_diva'),
        url(r'^diva_redo/$', 'diva_redo'),
        url(r'^login/$', 'user_login'),
        url(r'^logout/$', 'user_logout')
    )

urlpatterns += staticfiles_urlpatterns()
# urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'renamer.views.home', name='home'),
    # url(r'^renamer/', include('renamer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
# )
