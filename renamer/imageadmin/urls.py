"""imageadmin URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('manage/', views.manage, name='manage'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('to_archive/', views.to_archive, name='toarchive'),
    path('to_diva/', views.to_diva, name='todiva'),
    path('diva_redo/', views.diva_redo, name='divaredo'),
]
