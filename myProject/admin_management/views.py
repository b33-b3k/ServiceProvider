# D:\ServiceProvider\myProject\admin_management\views.py

from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import ServiceProvider, Tier
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime, timedelta
from booking.models import Appointment
from django.contrib.auth.decorators import login_required
from booking.models import VendorRequest


def vendor_requests_view(request):
    vendor_requests = VendorRequest.objects.all()
    return render(request, 'admindashBoard.html', {'items': vendor_requests})

def manage_service_providers(request):
    service_providers = ServiceProvider.objects.all()  # Retrieve all service providers from the database
    return render(request, 'admin_management/manage_service_providers.html', {'service_providers': service_providers})

def manage_tiers(request):
    tiers = Tier.objects.all()  # Retrieve all tiers from the database
    return render(request, 'admin_management/manage_tiers.html', {'tiers': tiers})

def index(request):
    return render(request, 'admin_management/index.html')


# def staffPanel(request):
#     today = datetime.today()
#     minDate = today.strftime('%Y-%m-%d')
#     deltatime = today + timedelta(days=21)
#     strdeltatime = deltatime.strftime('%Y-%m-%d')
#     maxDate = strdeltatime
#     #Only show the Appointments 21 days from today
#     items = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')

#     return render(request, 'admin_management/admindashBoard.html', {
#         'items':items,
#     })


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        # Use Django's built-in authentication.
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active and (user.is_staff or user.is_superuser):
                login(request, user)
                # Redirect to a dashboard or another page
                return redirect('admin-dashboard')
            else:
                messages.error(request, 'This account is not an admin.')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'admin_management/login_adm.html')

    # def logout_view(request):
    #     logout(request)
    #     return redirect('/') 



def dashboard_view(request):
    return render(request, 'admin_management/adminDashboard.html')

def staffPanel(request):
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime
    #Only show the Appointments 21 days from today
    items = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')

    return render(request, 'admindashBoard.html', {
        'items':items,
    })