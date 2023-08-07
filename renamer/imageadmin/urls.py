"""imageadmin URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('view_all_diva/', views.view_all_diva, name='view_all_diva'),
    path('view_diva/<str:document_id>', views.view_diva, name='view_diva'),
    path('view_ext_diva/<path:manifest_url>', views.view_ext_diva, name='view_ext_diva'),
    path('show_to_archive/', views.show_to_archive, name='show_to_archive'),
    path('show_to_diva/', views.show_to_diva, name='show_to_diva'),
    path('show_diva_redo/', views.show_diva_redo, name='show_diva_redo'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('to_archive/', views.to_archive, name='toarchive'),
    path('to_diva/', views.to_diva, name='todiva'),
    path('diva_redo/', views.diva_redo, name='divaredo'),
    path('view_task_result/<str:task_id>', views.view_task_result, name='view_task_result'),
]
