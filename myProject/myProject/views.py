from datetime import timedelta, timezone
import uuid
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.core.mail import send_mail



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
                return redirect('login-user')  # Redirect back to the login page if the authentication fails
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
        except User.DoesNotExist:
            user = None

        if user is not None:
            # Generate a unique token for the password reset link
            reset_token = str(uuid.uuid4())  # Convert the UUID4 to a string

            # Save the token and its expiration date in the user's profile or a separate password reset model
            user.profile.reset_token = reset_token
            user.profile.reset_token_expires_at = timezone.now() + timedelta(hours=1)
            user.profile.save()
            # Send an email to the user containing the password reset URL
            

            # Construct the password reset link using the token
            reset_link = f"http://127.0.0.1/reset_password/?token={reset_token}"

            # Send an email to the user with the password reset link
            # send_mail(
            #     'Password Reset Request',
            #     f'Please click the following link to reset your password: {reset_link}',
            #     'from@example.com',  # Replace with your email address
            #     [email],
            #     fail_silently=False,
            # )
            messages.success(request, "A password reset link has been sent to your email address.")
            return redirect('login')  # Redirect to the login page after sending the password reset link
        else:
            messages.error(request, "User with the provided email does not exist. Please try again.")
            return redirect('reset.html')  # Redirect back to the forgot password page if the user does not exist
    else:
        return render(request, 'forgot.html')  # Render the forgot password page for GET requests


def logout_view(request):
    logout(request)
    # Optionally, you can add a success message here
    return redirect('login') 