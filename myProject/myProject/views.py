from datetime import timedelta, timezone
import uuid
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.conf import settings

from django.contrib.auth import update_session_auth_hash



def home(request):
    # Your code logic goes here
    context = {
        'message': 'Hello, world!'
    }
    return render(request, 'index.html', context)

def about_view(request):
    return render(request, 'about.html')

def services_view(request):
    return render(request, 'service.html')

def contact_view(request):
    return render(request, 'contact.html')

def register_view(request):
    if request.method == 'GET':
        # Add the logic for handling the GET request
        return render(request, 'register.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username and email and password:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                messages.success(request, "User has been created successfully!")
                return redirect('login')  # Redirect to the login page after successful registration
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
                return redirect('register')  # Redirect back to the registration page if an error occurs
        else:
            messages.error(request, "Please fill in all the required fields.")
            return redirect('register')  # Redirect back to the registration page if the required fields are missing
    else:
        return HttpResponse("Method Not Allowed", status=405)  # Return an HTTP 405 Method Not Allowed for unsupported methods


def loginn(request):
    return render(request, 'choose_login.html')

def login_view(request):
    if request.method == 'GET':
        # Add the logic for handling the GET request
        return render(request, 'login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with the provided email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            # If the user exists, authenticate using the email and password
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been logged in successfully!")
                return redirect('booking')  # Redirect to the home page after successful login
            else:
                messages.error(request, "Invalid email or password. Please try again.")
                return redirect('login')  # Redirect back to the login page if the authentication fails
        else:
            messages.error(request, "User with the provided email does not exist. Please try again.")
            return redirect('login')  # Redirect back to the login page if the user does not exist
    else:
        return HttpResponse("Method Not Allowed", status=405)  # Return an HTTP 405 Method Not Allowed for unsupported methods



def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            request.session['reset_email'] = user.email  # Store the email in the session
            messages.success(request, "Please proceed to change your password.")
            return redirect('change_password')  # Redirect to the password change view
        except User.DoesNotExist:
            messages.error(request, "User with the provided email does not exist. Please try again.")
            return redirect('forgot_password')
    else:
        return render(request, 'forgot.html')





# Change Password View
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Retrieve the email from the session
        reset_email = request.session.get('reset_email')
        if not reset_email:
            messages.error(request, "No password reset request found.")
            return redirect('forgot_password')

        if new_password != confirm_password:
            messages.error(request, 'The two password fields didn’t match.')
            return render(request, 'reset.html')

        try:
            user = User.objects.get(email=reset_email)
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')  # Redirect to login page
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('forgot_password')
    else:
        return render(request, 'reset.html')
#faq
def faq_view(request):
    return render(request, 'faq.html')
    

def logout_view(request):
    logout(request)
    # Optionally, you can add a success message here
    return redirect('login') 