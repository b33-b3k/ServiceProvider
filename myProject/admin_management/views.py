# D:\ServiceProvider\myProject\admin_management\views.py

from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.db import IntegrityError
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime, timedelta
from booking.models import Staff
from django.contrib.auth.decorators import login_required
from booking.models import VendorRequest

from django.contrib.auth.models import User
from booking.models import Appointment
from booking.models import Staff
from booking.models import VendorRequest
from booking.models import Inquiry





def index(request):
    return render(request, 'admin_management/index.html')

def reject_vendor_request(request, vendor_email):
    # Retrieve all vendor requests with the given name
    vendor_requests = VendorRequest.objects.filter(email=vendor_email)

    # If there's only one match, delete it
    if vendor_requests.count() == 1:
        vendor_request = vendor_requests.first()
        vendor_request.delete()
        return redirect('admin-dashboard')

    # If there are multiple matches, handle them
    elif vendor_requests.count() > 1:
        vendor_request = vendor_requests.first()
        vendor_request.delete()
        return redirect('admin-dashboard')
        # For now, we'll just raise an error. You might want to handle this differently.
        

    # If there's no match, show a 404 error
    else:
        raise Http404("VendorRequest not found")

def accept_vendor_request(request, vendor_email):

    vendor_requests = VendorRequest.objects.filter(email=vendor_email)
  

    if not vendor_requests.exists():
        raise Http404("VendorRequest not found")

    vendor_request = vendor_requests.first()

    # Check if a staff member with this email already exists
    if Staff.objects.filter(email=vendor_email).exists():
        messages.error(request, "A staff member with this email already exists.")
        return redirect('admin-dashboard')

    try:
        Staff.objects.create(
            name=vendor_request.business_name,
            contact_number=vendor_request.contact_number,
            service=vendor_request.business_category,
            bio=vendor_request.business_description,
            email=vendor_email,  # Assuming your Staff model has an email field
            assigned_user=vendor_request.user,  # Associate the User from VendorRequest to the Staff
        )
        vendor_request.delete()
        messages.success(request, "Vendor request accepted successfully.")
        return redirect('admin-dashboard')
    except IntegrityError:
        messages.error(request, "An error occurred while processing the request. The staff member might already exist.")
        return redirect('admin-dashboard')
        

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

  



def dashboard_view(request):

    total_users = User.objects.count() 
    total_service_providers = Staff.objects.count()  
    pending_requests = VendorRequest.objects.count()
    vendor_requests = VendorRequest.objects.all()
    all_users = User.objects.all()

    try:
        vendor_data=Staff.objects.all()
    except Exception as e:
        print("Error",e)

        



    context={
        'vendor_requests':vendor_requests,
        'items':vendor_data,
        'users':all_users,
          'total_users': total_users,
        'total_service_providers': total_service_providers,
        'pending_requests': pending_requests
    }
   

    return render(request, 'admin_management/adminDashboard.html',context)

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

def delete_user(request,id):
    user=Staff.objects.get(id=id)
    user.delete()
    return redirect('admin-dashboard')