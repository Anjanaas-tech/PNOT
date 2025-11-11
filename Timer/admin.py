from django.contrib import admin  
from .models import Task  # Import the Task model

from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'created_at')  # Adjust based on your model
    list_filter = ('completed',)

admin.site.register(Task, TaskAdmin)

