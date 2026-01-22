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

def create_task(request):
    if request.method == 'POST':
        task_type = request.POST.get('task_type')
        title = request.POST.get('title')
        if task_type == 'normal':
            NormalTask.objects.create(title=title, user=request.user)
        elif task_type == 'continuous':
            ContinuousTask.objects.create(title=title, user=request.user)
    
    return render(request, 'tasks/create_task.html')