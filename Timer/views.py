from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Task  # Ensure models are imported correctly
from datetime import date

# Index view to list all tasks
def index(request):
    tasks = Task.objects.all()
    return render(request, 'timer/index.html', {'tasks': tasks})

# Custom login view with a specific template path
class CustomLoginView(LoginView):
    template_name = 'timer/registration/login.html'

# Register view for user registration
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')  # Phone is retrieved but not used in User creation
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password == password_confirm:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                messages.success(request, "Account created successfully!")
                return redirect('login')  # Ensure 'login' is the correct URL name
            else:
                messages.error(request, "Username already exists")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'timer/registration/register.html')

# View for displaying user tasks
def user_plan_view(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'timer/plan.html', {'tasks': tasks})

# View for displaying today's tasks
def today_tasks_view(request):
    tasks = Task.objects.filter(user=request.user, due_date=date.today())
    return render(request, 'timer/today_tasks.html', {'tasks': tasks})

# Calendar view
def calendar_view(request):
    return render(request, 'timer/calendar_view.html')

# Timer view
def timer_view(request):
    return render(request, 'timer/timer_view.html')

# Analytics view
def analytics_view(request):
    return render(request, 'timer/analytics.html')

# View to edit a task
def edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.due_date = request.POST.get('due_date')
        task.completed = request.POST.get('completed') == 'on'  # Handle checkbox input
        task.save()
        return render(request, 'timer/edit_task.html', {'task': task, 'success': True})

    return render(request, 'timer/edit_task.html', {'task': task})

# View to delete a task
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')  # Ensure 'task_list' is the correct URL name

    return render(request, 'timer/delete_task.html', {'task': task})
