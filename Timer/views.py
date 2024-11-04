from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views import View  
from django.contrib.auth.mixins import LoginRequiredMixin  
from datetime import date
from .models import Task, Goal, Note
from .forms import NoteForm
from .models import Note

# Custom login view with a specific template path
class CustomLoginView(LoginView):
    template_name = 'timer/registration/login.html'

# Register view for user registration
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password == password_confirm:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                messages.success(request, "Account created successfully!")
                return redirect('login')  # Ensure 'login' matches the URL name for the login view
            else:
                messages.error(request, "Username already exists")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'timer/registration/register.html')

# Index view to list all tasks
def index(request):
    tasks = Task.objects.all()
    return render(request, 'timer/index.html', {'tasks': tasks})

# View for displaying user tasks
@login_required
def user_plan(request):
    tasks = Task.objects.filter(user=request.user)  # Show tasks only for the logged-in user
    return render(request, 'timer/plan.html', {'tasks': tasks})

# View for displaying today's tasks
@login_required
def today_tasks_view(request):
    tasks = Task.objects.filter(user=request.user, due_date=date.today())
    return render(request, 'timer/today_tasks.html', {'tasks': tasks})

# Calendar view
def calendar_view(request):
    return render(request, 'timer/calendar_view.html')

# Timer view
def timer_view(request):
    return render(request, 'timer/timer.html')

# Schedule view
def schedule_view(request):
    return render(request, 'timer/schedule.html')

# View to delete a task
@login_required
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect('user_plan')  # Ensure this matches the correct URL name
    return render(request, 'timer/delete_task.html', {'task': task})

# Add a new goal
@login_required
def add_goal(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            Goal.objects.create(user=request.user, title=title, description=description)
            messages.success(request, 'Goal added successfully!')
            return redirect('goals')  # Ensure this matches the correct URL name
    return render(request, 'timer/goals.html')

# Mark goal as completed
@login_required
def complete_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    goal.completed = True
    goal.save()
    messages.success(request, "Goal marked as completed!")
    return redirect('goals')

# Delete a goal
@login_required
def delete_goal(request, id):
    goal = get_object_or_404(Goal, id=id)
    if request.method == "POST":
        goal.delete()
        messages.success(request, "Goal deleted successfully!")
        return redirect('goals')
    return render(request, 'timer/confirm_delete.html', {'goal': goal})

# View goals with progress calculation
@login_required
def goal_view(request):
    goals = Goal.objects.filter(user=request.user)
    progress_percentage = calculate_progress(goals)
    return render(request, 'timer/goals.html', {'goals': goals, 'progress_percentage': progress_percentage})

# Helper function to calculate progress
def calculate_progress(goals):
    total_goals = goals.count()
    completed_goals = goals.filter(completed=True).count()
    return (completed_goals / total_goals) * 100 if total_goals > 0 else 0

# Set a weekly goal
@login_required
def set_weekly_goal(request):
    if request.method == "POST":
        goal = request.POST.get('goal')
        if goal:
            save_weekly_goal(request.user, goal)
            messages.success(request, 'Your weekly goal has been set!')
            return redirect('set_weekly_goal')
        else:
            messages.error(request, 'Please enter a goal.')
    return render(request, 'timer/goals.html')

# Helper function to save the weekly goal
def save_weekly_goal(user, goal):
    Goal.objects.create(user=user, title="Weekly Goal", description=goal)

# Complete task view
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    messages.success(request, "Task marked as completed!")
    return redirect('user_plan')

# Notes-related views
@login_required
def add_note_view(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, 'Note added successfully!')
            return redirect('notes')
    else:
        form = NoteForm()
    return render(request, 'timer/add_note.html', {'form': form})

@login_required
def notes_view(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'timer/notes.html', {'notes': notes})

# View to delete a note using AJAX
@csrf_exempt
@login_required
def delete_note(request, note_id):
    if request.method == 'DELETE':
        try:
            note = Note.objects.get(id=note_id, user=request.user)
            note.delete()
            return JsonResponse({'success': True})
        except Note.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Note does not exist'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

from .models import Note

def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        # Process form submission to edit the note here
        # Example:
        note.content = request.POST.get('content', '')
        note.save()
        return redirect('notes')
    return render(request, 'Timer/edit_note.html', {'note': note})
