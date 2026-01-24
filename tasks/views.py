
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import NormalTask, ContinuousTask
from .forms import NormalTaskForm, ContinuousTaskForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import random


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'tasks/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'tasks/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'tasks/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def create_task(request):
    if request.method == 'POST':
        task_type = request.POST.get('task_type')
        if task_type == 'normal':
            normal_task_form = NormalTaskForm(request.POST)
            if normal_task_form.is_valid():
                normal_task = normal_task_form.save(commit=False)
                normal_task.user = request.user
                normal_task.save()
                messages.success(request, 'Normal task created successfully.')
                return redirect('dashboard')

        elif task_type == 'continuous':
            continuous_task_form = ContinuousTaskForm(request.POST)
            if continuous_task_form.is_valid():
                continuous_task = continuous_task_form.save(commit=False)
                continuous_task.user = request.user
                continuous_task.save()
                messages.success(request, 'Continuous task created successfully.')
                return redirect('dashboard')

    return redirect('dashboard')

@login_required
def dashboard(request):
    normal_tasks = NormalTask.objects.filter(user=request.user)
    continuous_tasks = ContinuousTask.objects.filter(user=request.user)
    normal_task_form = NormalTaskForm()
    continuous_task_form = ContinuousTaskForm()
    not_started_normal = NormalTask.objects.filter(
        user=request.user, completed=False
    )
    not_started_continuous = ContinuousTask.objects.filter(
        user=request.user, completed=False, work_time=0
    )
    not_started = list(not_started_normal) + list(not_started_continuous)

    on_going = ContinuousTask.objects.filter(user=request.user, work_time__gt=0, completed=False)

    completed_normal = NormalTask.objects.filter(
        user=request.user, completed=True
    )
    completed_continuous = ContinuousTask.objects.filter(
        user=request.user, completed=True
    )
    completed = list(completed_normal) + list(completed_continuous)

    context = {
        'normal_tasks': normal_tasks,
        'continuous_tasks': continuous_tasks,
        'normal_task_form': normal_task_form,
        'continuous_task_form': continuous_task_form,
        'not_started': not_started,
        'on_going': on_going,
        'completed': completed,
    }
    return render(request, 'tasks/dashboard.html', context)


@login_required
def edit_task(request, task_id, task_type):
    if task_type == 'normal':
        task = get_object_or_404(NormalTask, id=task_id, user=request.user)
        form_class = NormalTaskForm
    else:
        task = get_object_or_404(ContinuousTask, id=task_id, user=request.user)
        form_class = ContinuousTaskForm

    if request.method == 'POST':
        form = form_class(request.POST, instance=task)
        if form.is_valid():
            updated_task = form.save(commit=False)
            updated_task.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('dashboard')
    else:
        form = form_class(instance=task)

    return render(request, 'tasks/edit_task.html', {
        'form': form,
        'task_id': task_id,
        'task_type': task_type,
    })


@login_required
def delete_task(request, task_id, task_type):
    if request.method == 'POST':
        if task_type == 'normal':
            task = get_object_or_404(NormalTask, id=task_id, user=request.user)
        else:
            task = get_object_or_404(ContinuousTask, id=task_id, user=request.user)

        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('dashboard')

    return redirect('dashboard')


@login_required
def dice_roll(request):
    if request.method == 'POST':
        session = request.session
        tasks = list(
            NormalTask.objects.filter(user=request.user, completed=False)
        )
        tasks.extend(
            list(ContinuousTask.objects.filter(user=request.user, completed=False))
        )
        digit = random.randint(1, 4)
        if digit == 1 or not tasks:
            session['result'] = {'type': 'break'}
        else:
            random_task = random.choice(tasks)
            task_type = (
                'normal' if isinstance(random_task, NormalTask) else 'continuous'
            )
            session['result'] = {
                'type': 'task',
                'task_id': random_task.id,
                'task_type': task_type,
                'task_title': random_task.title,
            }
    return redirect('dashboard')


@login_required
def complete_task(request, task_id, task_type):
    if request.method == 'POST':
        if task_type == 'normal':
            task = get_object_or_404(NormalTask, id=task_id, user=request.user)
        elif task_type == 'continuous':
            task = get_object_or_404(ContinuousTask, id=task_id, user=request.user)
        else:
            return redirect('dashboard')
        task.completed = True
        task.save()
        messages.success(request, 'Task marked as completed.')
        request.session.pop('result', None)
    return redirect('dashboard')


@login_required
def increment_work_time(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(ContinuousTask, id=task_id, user=request.user)
        task.work_time += 1
        task.save()
        messages.success(request, f'Work time increased to {task.work_time} hours.')
    return redirect('dashboard')

