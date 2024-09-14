from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Task


# Index view to list all tasks
def index(request):
    tasks = Task.objects.all()
    return render(request, 'timer/index.html', {'tasks': tasks})

# Custom login view with a specific template path
class CustomLoginView(LoginView):
    template_name = 'timer/registration/login.html'  # Use a relative path

from django.shortcuts import render

def my_view(request):
    if request.method == 'POST':
        # Process the form submission
        pass
    return render(request, 'base.html')


# Register view for user registration
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password == password_confirm:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                messages.success(request, "Account created successfully!")
                return redirect('login')  # Change 'login' to the actual name of your login URL
            else:
                messages.error(request, "Username already exists")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'timer/registration/register.html')  # Ensure this path is correct

