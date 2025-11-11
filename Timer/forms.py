from django import forms
from .models import Task
from .models import Note

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'due_date']  # Include due_date here


from django import forms
from .models import Note  # Ensure your Note model is imported

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']  # Add any additional fields as necessary

    # Optional: Add custom validation or widgets if needed
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Title is required.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("Content is required.")
        return content


