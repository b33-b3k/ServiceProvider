from django.shortcuts import render
from django.http import HttpResponse

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
    return render(request, 'register.html')

def login_view(request):
    return render(request, 'login.html')



def forgot_password_view(request):
    return render(request, 'forgot.html')