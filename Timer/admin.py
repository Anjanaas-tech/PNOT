from django.contrib import admin
from .models import Task, Note, Goal

# Admin configuration for Task model
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'created_at')  # Adjust based on your model
    list_filter = ('completed',)

# Register models with the admin site
admin.site.register(Task, TaskAdmin)
admin.site.register(Note)
admin.site.register(Goal)


