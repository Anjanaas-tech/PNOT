from django.contrib import admin
from .models import Task, Note, Goal,Schedule,Event

# Register models with the admin site
admin.site.register(Task)
admin.site.register(Note)
admin.site.register(Goal)
admin.site.register(Schedule)
admin.site.register(Event)


