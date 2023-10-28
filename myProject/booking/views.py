from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import *
from django.contrib import messages
from .models import * # Import your model class

from .forms import *


def vendor_dashboard(request):
    # Fetch appointments associated with the logged-in vendor
    try:
        # Fetch appointments associated with the logged-in vendor
        appointments = Appointment.objects.all()
        all_vendor_requests = VendorRequest.objects.all()
        staffs=Staff.objects.all()

        print(appointments)
    except Appointment.DoesNotExist:
        # Handle the case where no appointments are found for the vendor
        appointments = []
    except Exception as e:
        # Handle other unexpected database errors
        return HttpResponseBadRequest(f"An error occurred: {e}")
    context = {
        'appointments': appointments,
        'vendor_requests': all_vendor_requests,
        'items': staffs,
        
    }
    return render(request, 'vendordashBoard.html', context)

def submit_staff_data(request):
    if request.method == 'POST':
        staff_name = request.POST.get('staff_name')
        print(staff_name)
        try:
            staff_member = Staff.objects.get(name=staff_name)
            
            # Create a new appointment
            appointment = Appointment.objects.create(
                user=request.user,
                service=staff_member.service,
                staff=staff_member.name,
            )
            
            # You can add additional logic here if needed

            return redirect('booking') 
        except Staff.DoesNotExist:
            # Handle the case where no staff with the given name exists
            # For example, you can return an error message or redirect to another page
            return HttpResponse("Staff with the given name does not exist.")


def vendor_requests_view(request):
    vendor_requests = VendorRequest.objects.all()
    return render(request, 'admindashBoard.html', {'items': vendor_requests})

def become_vendor(request):
    print(request.POST)

    if request.method == 'POST':
        business_name = request.POST.get('business_name')
        business_address = request.POST.get('business_address')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        business_description = request.POST.get('business_description')
        business_category = request.POST.get('business_category')
        pan_number = request.POST.get('pan_number')

        # Check if required fields are not empty
        if not business_name or not business_address or not contact_number:
            messages.error(request, 'Please fill out all required fields.')
        else:
            # Create and save the VendorRequest instance
            vendor_request = VendorRequest(
                user=request.user,  # Assign the current user
                business_name=business_name,
                business_address=business_address,
                contact_number=contact_number,
                email=email,
                business_description=business_description,
                business_category=business_category,
                pan_number=pan_number,
            )
            vendor_request.save()
            messages.success(request, 'Vendor request submitted successfully.')
            return redirect('booking')  # Redirect to a success view or page

    return render(request, 'become_vendor.html')




def index(request):
    return render(request, "vendordashBoard.html",{})

def logout_view(request):
    logout(request)
    # Redirect to a success page or some other page
    return redirect('login') 


def booking(request):

    weekdays = validWeekday(7)
    validateWeekdays = isWeekdayValid(weekdays)
    times = [        "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM", "6:30 PM", "7 PM", "7:30 PM"]
    address = ""  # Add this line to include address in the context

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')
        time = request.POST.get('time')
        address = request.POST.get('address')

        
     
        print("Service: ", service)
        print("Day: ", day)
        print("Time: ", time)
        print("Address: ", address)   

        if service is None:
            messages.success(request, "Please Select A Service!")
            return redirect('booking')

        request.session['day'] = day
        request.session['service'] = service
        request.session['time'] = time
        request.session['address'] = address

         # Save the data to the Appointment model
        appointment = Appointment.objects.create(
            user=request.user,
            service=service,
            day=day,
            time=time,
            staff="Not assigned",
        )

        return redirect('bookingSubmit')


    return render(request, 'booking.html', {
    'weekdays': weekdays,
    'validateWeekdays': validateWeekdays,
    'times': times,  # Add this line to include time in the context
    'address': address  # Add this line to include address in the context
})



def bookingSubmit(request):
    user = request.user
    times = [
        "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM", "6:30 PM", "7 PM", "7:30 PM"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    # Get stored data from django session:
    day = request.session.get('day')
    service = request.session.get('service')
    staff_members = Staff.objects.all()

    if request.method == 'POST':
        time = request.POST.get("time")
        staff_name = request.POST.get('staff_name')

        print(staff_name)

        # Save the staff_name to the session

        # Assuming dayToWeekday is a function you've defined elsewhere
        date = dayToWeekday(day)

        # Create or update the appointment
        if service != None:
            if day <= maxDate and day >= minDate:
                
                        if Appointment.objects.filter(day=day, time=time).count() < 1:
                            AppointmentForm = Appointment.objects.filter(user=user).update(
                                user = user,
                                service = service,
                                day = day,
                                time = time,
                                staff = staff_name,
                            ) 
                            messages.success(request, "Appointment Booked!")
                            return redirect('booking')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    
            else:
                    messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Service!")

        return redirect('booking')

    return render(request, 'bookingSubmit.html', {
        'times': times, 'staff': staff_members
    })

def userPanel(request):
    user = request.user
    appointments = Appointment.objects.filter(user=user).order_by('day', 'time')
    return render(request, 'userPanel.html', {
        'user':user,
        'appointments':appointments,
    })
def userUpdate(request, id):
    appointment = Appointment.objects.get(pk=id)
    
    # Convert the appointment.day string to a datetime object
    userdatepicked = datetime.strptime(appointment.day, '%Y-%m-%d')
    
    # Copy booking:
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')


    # 24h if statement in template:
    delta24 = userdatepicked.strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)

    # Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)
    
    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')

        # Store day and service in django session:
        request.session['day'] = day
        request.session['service'] = service

        return redirect('userUpdateSubmit', id=id)

    return render(request, 'userUpdate.html', {
            'weekdays': weekdays,
            'validateWeekdays': validateWeekdays,
            'delta24': delta24,
            'id': id,
            
        })


def userUpdateSubmit(request, id):
    user = request.user
    times = [
        "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM", "6:30 PM", "7 PM", "7:30 PM"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    day = request.session.get('day')
    service = request.session.get('service')
    
    #Only show the time of the day that has not been selected before and the time he is editing:
    hour = checkEditTime(times, day, id)
    appointment = Appointment.objects.get(pk=id)
    userSelectedTime = appointment.time
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if service != None:
         
                        if Appointment.objects.filter(day=day, time=time).count() < 1 or userSelectedTime == time:
                            AppointmentForm = Appointment.objects.filter(pk=id).update(
                                user = user,
                                service = service,
                                day = day,
                                time = time,
                            ) 
                            messages.success(request, "Appointment Edited!")
                            return redirect('index')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                 
        else:
            messages.success(request, "Please Select A Service!")
        return redirect('userPanel')


    return render(request, 'userUpdateSubmit.html', {
        'times':hour,
        'id': id,
    })



def dayToWeekday(x):
    z = datetime.strptime(x, "%Y-%m-%d")
    y = z.strftime('%A')
    return y

def validWeekday(days):
    #Loop days you want in the next 21 days:
    today = datetime.now()
    weekdays = []
    for i in range (0, days):
        x = today + timedelta(days=i)
        y = x.strftime('%A')
        if y == 'Monday' or y == 'Tuesday' or y == 'Wednesday'or y == 'Thursday' or y == 'Friday'or y == 'Saturday':
            weekdays.append(x.strftime('%Y-%m-%d'))
    return weekdays
    
def isWeekdayValid(x):
    validateWeekdays = []
    for j in x:
        if Appointment.objects.filter(day=j).count() < 10:
            validateWeekdays.append(j)
    return validateWeekdays

def checkTime(times, day):
    #Only show the time of the day that has not been selected before:
    x = []
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1:
            x.append(k)
    return x

def checkEditTime(times, day, id):
    #Only show the time of the day that has not been selected before:
    x = []
    appointment = Appointment.objects.get(pk=id)
    time = appointment.time
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x
