# D:\ServiceProvider\myProject\admin_management\urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('service-providers/', views.manage_service_providers, name='manage_service_providers'),
    path('tiers/', views.manage_tiers, name='manage_tiers'),
    


    # Add other URLs as needed



    #only for admin
    
]
