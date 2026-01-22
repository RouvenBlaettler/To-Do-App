from django import forms
from .models import NormalTask, ContinuousTask

class TaskForm(forms.ModelForm):
    class Meta:
        model = NormalTask
        fields = ['title', 'completed']

class ContinuousTaskForm(forms.ModelForm):
    class Meta:
        model = ContinuousTask
        fields = ['title', 'work_time', 'completed', 'task_type']