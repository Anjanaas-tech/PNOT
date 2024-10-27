from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Task, Goal  # Ensure models are imported correctly
from .forms import TaskForm
from datetime import date
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm


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
@login_required
def user_plan_view(request):
    tasks = Task.objects.all()  # or the appropriate queryset
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
    return render(request, 'timer/timer_view.html')

# Analytics view
def analytics_view(request):
    return render(request, 'timer/analytics.html')


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
            Goal.objects.create(user=request.user, title=title, description=description)  # Tie goal to user
            messages.success(request, 'Goal added successfully!')
            return redirect('goals')  # Ensure this matches the correct URL name
    return render(request, 'timer/goals.html')

# Mark goal as completed
@login_required
def complete_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    goal.completed = True
    goal.save()
    messages.success(request, "Goal marked as completed!")  # Add success message
    return redirect('goals')  # Ensure this matches your urls.py

# Delete a goal
@login_required
def delete_goal(request, id):
    goal = get_object_or_404(Goal, id=id)  # This will return a 404 if the goal does not exist
    if request.method == "POST":
        goal.delete()
        messages.success(request, "Goal deleted successfully!")  # Add success message
        return redirect('goals')  # Redirect after deletion
    return render(request, 'timer/confirm_delete.html', {'goal': goal})

# View goals
@login_required
def goal_view(request):
    goals = Goal.objects.filter(user=request.user)  # Show only user's goals
    progress_percentage = calculate_progress(goals)  # Helper to calculate progress
    return render(request, 'timer/goals.html', {'goals': goals, 'progress_percentage': progress_percentage})

# Helper function to calculate progress
def calculate_progress(goals):
    total_goals = goals.count()
    completed_goals = goals.filter(completed=True).count()
    if total_goals > 0:
        return (completed_goals / total_goals) * 100
    return 0

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
    task.is_completed = True  # Assuming 'is_completed' is a field in your Task model
    task.save()
    messages.success(request, "Task marked as completed!")
    return redirect('user_plan')  # Ensure this matches the correct URL name


@login_required
def add_note_view(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  # Assign the logged-in user to the note
            note.save()
            return redirect('notes')  # Redirect to the list of notes
    else:
        form = NoteForm()  # Create a new form instance for GET requests

    return render(request, 'Timer/add_note.html', {'form': form})

@login_required
def notes_view(request):
    notes = Note.objects.filter(user=request.user)  # Get notes for the logged-in user
    return render(request, 'Timer/notes.html', {'notes': notes})
