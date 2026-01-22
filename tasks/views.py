from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import NormalTask, ContinuousTask
from .forms import NormalTaskForm, ContinuousTaskForm


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            return render(request, 'tasks/register.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'tasks/register.html', {'error': 'Username already exists'})
        
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('dashboard')
    
    return render(request, 'tasks/register.html')


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
def dashboard(request):
    normal_tasks = NormalTask.objects.filter(user=request.user)
    continuous_tasks = ContinuousTask.objects.filter(user=request.user)
    normal_task_form = NormalTaskForm()
    continuous_task_form = ContinuousTaskForm()
    
    if request.method == 'POST':
        task_type = request.POST.get('task_type')
        
        if task_type == 'normal':
            normal_task_form = NormalTaskForm(request.POST)
            if normal_task_form.is_valid():
                normal_task = normal_task_form.save(commit=False)
                normal_task.user = request.user
                normal_task.save()
                return redirect('dashboard')

        elif task_type == 'continuous':
            continuous_task_form = ContinuousTaskForm(request.POST)
            if continuous_task_form.is_valid():
                continuous_task = continuous_task_form.save(commit=False)
                continuous_task.user = request.user
                continuous_task.save()
                return redirect('dashboard')
            

    context = {
        'normal_tasks': normal_tasks,
        'continuous_tasks': continuous_tasks,
        'normal_task_form': normal_task_form,
        'continuous_task_form': continuous_task_form,
    }
    return render(request, 'tasks/dashboard.html', context)