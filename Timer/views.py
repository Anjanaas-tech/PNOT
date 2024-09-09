from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
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
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a success page or home
    else:
        form = UserCreationForm()
        return render(request, 'timer/register.html', {'form': form, 'current_year': 2024})




