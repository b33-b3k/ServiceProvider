from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404
from .models import * # Import your model class
from .forms import *



def login_view(request):
    if request.method == 'GET':
        return render(request, 'loginServiceProvider.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with the provided email exists in the User model
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User with the provided email does not exist. Please try again.")
            return redirect('login-provider')  # Redirect back to the login page if the user does not exist

        # Authenticate the user using the email and password
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            # Check if the user's email exists in the Staff model
            try:
                staff_member = Staff.objects.get(email=email)
                # If the user is a staff member, proceed with login
                login(request, user)
                messages.success(request, "You have been logged in successfully as staff!")
                return redirect('dashboard-panel')  # Redirect to the dashboard panel after successful login
            except Staff.DoesNotExist:
                # The user exists but is not listed as a staff member in the Staff model
                messages.error(request, "You do not have staff access. Please contact the administrator.")
                return redirect('login-provider')  # Redirect back to the login page if the user is not a staff member
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('login-provider')  # Redirect back to the login page if the authentication fails
    else:
        return HttpResponse("Method Not Allowed", status=405)  # Return an HTTP 405 Method Not Allowed for unsupported methods


    


def vendor_dashboard(request):
    # Fetch the staff member associated with the logged-in user
    items = Inquiry.objects.all()

    try:
        # Make the name field case-insensitive
        staff_member = Staff.objects.get(name__iexact=request.user.username)
        print(request.user.username)
    except Staff.DoesNotExist:
        # Handle case where logged-in user is not a staff member
        return HttpResponseBadRequest("You are not registered as a staff member.")

    try:
        # Fetch appointments associated with the logged-in staff member
        appointments = Appointment.objects.filter(staff=staff_member.name)
        print(staff_member)
    except Appointment.DoesNotExist:
        # Handle the case where no appointments are found for the staff member
        appointments = []

    context = {
        'appointments': appointments,
        'staff_member': staff_member,
        "items": items
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
        # name 
        business_name= request.POST.get("username")


        
        business_address = request.POST.get('business_address')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        business_description = request.POST.get('business_description')
        business_category = request.POST.get('business_category')
        pan_number = request.POST.get('pan_number')

        # Check if required fields are not empty


        #check if vendor request already exist
        if VendorRequest.objects.filter(user=request.user).exists():
            messages.error(request, "You have already submitted a vendor request.")
        else:

        
            # Create and save the VendorRequest instance
            vendor_request = VendorRequest(
                user=request.user,  # Assign the current user,
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
    times = [
        "9 am",
        "10 am",
        "11 am",
        "12 pm",
        "1 pm",
        "2 pm",
        "3 pm",
        "4 pm"
    ]
    staff_members = Staff.objects.all()  # Query all staff members

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
            staff="Not assigned",  # You might want to assign a staff member here
        )

        return redirect('bookingSubmit')

    return render(request, 'booking.html', {
        'weekdays': weekdays,
        'validateWeekdays': validateWeekdays,
        'times': times,
        'staff_members': staff_members,  # Add this line to include staff in the context
    })

def bookingSubmit(request):
    user = request.user
    times = [
        "9 am",
        "10 am",
        "11 am",
        "12 pm",
        "1 pm",
        "2 pm",
        "3 pm",
        "4 pm"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    # Get stored data from django session:
    day = request.session.get('day')
    service = request.session.get('service')
    print(service)

    # Filter staff members based on the selected service
    if service == 'Plumber':
        staff_members = Staff.objects.filter(service='Plumber')
    elif service == 'Electrician':
        staff_members = Staff.objects.filter(service='Electrician')
    else:
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
                
                      appointment, created = Appointment.objects.get_or_create(
            day=day, 
            time=time, 
            defaults={
                'user': user,
                'service': service,
                'staff': staff_name,
            })
                    
            else:
                    messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Service!")

        return redirect('booking')

    return render(request, 'bookingSubmit.html', {
        'times': times, 'staff': staff_members,
        
    })
def userPanel(request):
    user = request.user
    appointments = Appointment.objects.filter(user=user).order_by('day', 'time')
    return render(request, 'userPanel.html', {
        'user':user,
        'appointments':appointments,
    })



def inquirySubmit(request):
    if request.method == 'POST':
        print(request.POST)  # This will print the POST data to the console

        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')
        print(f"Staff ID: {staff_id}, Message: {message}")  # Check what you're getting here


        if staff_id and message:
            staff_member = get_object_or_404(Staff, pk=staff_id)
            try:
                # Assuming 'inquiry_message' is a field in your StaffMember model
                staff_member.inquiry_message = message
                staff_member.save()
                messages.success(request, "Your message has been sent to the staff member.")
                return redirect('booking')  # Redirect to the contact page after successful submission
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
                return redirect('booking')  # Redirect back to the contact page if an error occurs
        else:
            messages.error(request, "Please provide a message.")
            return redirect('booking')  # Redirect back to the contact page if the message is missing
    else:
        return HttpResponse("Method Not Allowed", status=405)  # Return an HTTP 405 Method Not Allowed for unsupported methods
def userUpdate(request, id):
    appointment = Appointment.objects.get(pk=id)
    
    # Convert the appointment.day string to a datetime object
    # userdatepicked = datetime.strptime(appointment.day, '%Y-%m-%d')
    
    # Copy booking:
    today = datetime.today()
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
            # 'delta24': delta24,
            'id': id,
            
        })

def appointmentDelete(request,id):
    appointment = Appointment.objects.get(pk=id)
    appointment.delete()
    messages.success(request, "Appointment Deleted!")
    return redirect('dashboard-panel')

def appointmentDeleteBooking(request,id):
    appointment = Appointment.objects.get(pk=id)
    appointment.delete()
    messages.success(request, "Appointment Deleted!")
    return redirect('booking')

def inquiryDelete(request, id):
    try:
        appointment = Appointment.objects.get(pk=id)
        
        messages.success(request, "Inquiry Deleted!")
        return redirect('dashboard-panel')
    except:
        # Handle the case where the inquiry does not exist
        messages.error(request, "Inquiry does not exist")
        
        return redirect('dashboard-panel')  # Redirect to the appropriate page



def appointmentFinished(request,id):
    #make it take the appointment throgu id and make a field true
    appointment = Appointment.objects.get(pk=id)
    appointment.isFinished = "Yes"
    appointment.save()
    messages.success(request, "Appointment Finished!")
    return redirect('dashboard-panel')
    



def userUpdateSubmit(request, id):
    user = request.user
    times = [
        "9 am ",
        "10 am ",
        "11 am ",
        "12 pm ",
        "1 pm ",
        "2 pm ",
        "3 pm ",
        "4 pm "
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

                            return redirect('booking')
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
