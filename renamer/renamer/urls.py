#from django.conf.urls import patterns, include, url, static
#from django.conf import settings
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('imageadmin/', include('imageadmin.urls')),
    path('admin/', admin.site.urls),
]

#base_urlpatterns = []
#if 'django.contrib.admin' in settings.INSTALLED_APPS:
#    base_urlpatterns += patterns('',
#        url(r'^admin/', include(admin.site.urls))
#    )

#base_urlpatterns += patterns('renamer.views.main',
#     url(r'^$', 'home', name="home"),
#     url(r'^manage/*$', 'manage', name="manage"),
#     url(r'^to_archive/*$', 'to_archive'),
#     url(r'^to_diva/*$', 'to_diva'),
#     url(r'^diva_redo/*$', 'diva_redo'),
#     url(r'^login/*$', 'user_login'),
#     url(r'^logout/*$', 'user_logout')
# )
#
# urlpatterns = patterns('',
#         url(r'^imageadmin/', include(base_urlpatterns))
#     )
#
# urlpatterns += staticfiles_urlpatterns()
