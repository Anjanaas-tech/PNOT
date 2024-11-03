from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import add_note_view, notes_view
from .views import schedule_view


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='timer/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('plan/', views.user_plan, name='user_plan'),
    path('today_tasks/', views.today_tasks_view, name='today_tasks'),
    path('calendar_view/', views.calendar_view, name='calendar_view'),
    path('timer/', views.timer_view, name='timer'),
    path('schedule/', schedule_view, name='schedule'),
    path('delete_task/<int:task_id>/', views.delete_task_view, name='delete_task'),
    path('goals/', views.goal_view, name='goals'),
    path('add_goal/', views.add_goal, name='add_goal'),
    path('complete_goal/<int:goal_id>/', views.complete_goal, name='complete_goal'),
    path('delete_goal/<int:id>/', views.delete_goal, name='delete_goal'),
    path('set-weekly-goal/', views.set_weekly_goal, name='set_weekly_goal'),
    path('notes/', views.notes_view, name='notes'),
    path('notes/add/', views.add_note_view, name='add_note'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
]
