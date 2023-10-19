# D:\ServiceProvider\myProject\admin_management\views.py

from django.shortcuts import render
from .models import ServiceProvider, Tier

def manage_service_providers(request):
    service_providers = ServiceProvider.objects.all()  # Retrieve all service providers from the database
    return render(request, 'admin_management/manage_service_providers.html', {'service_providers': service_providers})

def manage_tiers(request):
    tiers = Tier.objects.all()  # Retrieve all tiers from the database
    return render(request, 'admin_management/manage_tiers.html', {'tiers': tiers})

def index(request):
    return render(request, 'admin_management/index.html')

