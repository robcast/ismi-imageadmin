"""imageadmin URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('manage/', views.manage, name='manage'),
    path('show_to_archive/', views.show_to_archive, name='show_to_archive'),
    path('show_to_diva/', views.show_to_diva, name='show_to_diva'),
    path('show_diva_redo/', views.show_diva_redo, name='show_diva_redo'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('to_archive/', views.to_archive, name='toarchive'),
    path('to_diva/', views.to_diva, name='todiva'),
    path('diva_redo/', views.diva_redo, name='divaredo'),
]
