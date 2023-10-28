# D:\ServiceProvider\myProject\admin_management\urls.py

from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('login-admin/', views.admin_login, name='login-admin'),

    #dashboard
    path('dashboard-admin/', views.dashboard_view, name='admin-dashboard'),
    path('accept_vendor_request/<str:vendor_name>/', views.accept_vendor_request, name='accept_vendor_request'),
    path('admin/reject_vendor_request/<str:vendor_name>/', views.reject_vendor_request, name='reject_vendor_request'),


    
    # path('staff-panel/', views.staffPanel, name='staff-panel'),
    


    # Add other URLs as needed



    #only for admin
    
]
