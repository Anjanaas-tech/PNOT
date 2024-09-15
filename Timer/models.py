from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Add this field
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    
