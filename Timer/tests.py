from django.test import TestCase
from .models import Task

class TaskModelTest(TestCase):
    def test_string_representation(self):
        task = Task(title="My Task")
        self.assertEqual(str(task), task.title)
