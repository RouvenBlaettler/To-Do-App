from django.shortcuts import render
from .models import NormalTask, ContinuousTask

def task_list(request):
    normal_tasks = NormalTask.objects.all()
    continuous_tasks = ContinuousTask.objects.all()
    context = {
        'normal_tasks': normal_tasks,
        'continuous_tasks': continuous_tasks,
    }
    return render(request, 'tasks/home.html', context)