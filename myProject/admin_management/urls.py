# D:\ServiceProvider\myProject\admin_management\urls.py

from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('login-admin/', views.admin_login, name='login-admin'),

    #dashboard
    path('dashboard-admin/', views.dashboard_view, name='admin-dashboard'),
    path('accept_vendor_request/<str:vendor_email>/', views.accept_vendor_request, name='accept_vendor_request'),
    path('reject_vendor_request/<str:vendor_email>/', views.reject_vendor_request, name='reject_vendor_request'),
    
    #delete user
    path('delete-user/<int:id>/', views.delete_user, name='delete-user'),



    
    
]
