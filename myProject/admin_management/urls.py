# D:\ServiceProvider\myProject\admin_management\urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('service-providers/', views.manage_service_providers, name='manage_service_providers'),
    path('tiers/', views.manage_tiers, name='manage_tiers'),
    path('login-admin/', views.admin_login, name='login-admin'),

    #dashboard
    path('dashboard-admin/', views.dashboard_view, name='admin-dashboard'),
    # path('staff-panel/', views.staffPanel, name='staff-panel'),
    


    # Add other URLs as needed



    #only for admin
    
]
