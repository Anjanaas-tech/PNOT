from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
   path('login/', auth_views.LoginView.as_view(template_name='timer/login.html'), name='login'),
   path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   path('register/', views.register, name='register'),
    path('plan/', views.user_plan_view, name='user_plan'),
    path('today_tasks/', views.today_tasks_view, name='today_tasks'),
    path('calendar_view/', views.calendar_view, name='calendar_view'),
    path('timer/', views.timer_view, name='timer'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('edit_task/<int:task_id>/', views.edit_task_view, name='edit_task'),
    path('delete_task/<int:task_id>/', views.delete_task_view, name='delete_task'),
    
]   

