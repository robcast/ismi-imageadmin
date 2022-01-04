#from django.conf.urls import patterns, include, url, static
#from django.conf import settings
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('imageadmin/', include('imageadmin.urls')),
    path('imageadmin/admin/', admin.site.urls),
]
