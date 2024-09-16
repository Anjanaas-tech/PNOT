from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Add this field
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    
