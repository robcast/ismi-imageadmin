from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('imageadmin/', include('imageadmin.urls')),
    path('imageadmin/admin/', admin.site.urls),
]
