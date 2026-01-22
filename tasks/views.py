from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import NormalTask, ContinuousTask
from .forms import NormalTaskForm, ContinuousTaskForm
from django.contrib.auth.forms import UserCreationForm


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Create new user
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, "pages/register.html", {
        "form": form
    })

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
        print(f"Task type selected: {task_type}")
        print(f"POST data: {request.POST}")
        
        if task_type == 'normal':
            normal_task_form = NormalTaskForm(request.POST)
            if normal_task_form.is_valid():
                normal_task = normal_task_form.save(commit=False)
                normal_task.user = request.user
                normal_task.save()
                print(f"Normal task created: {normal_task.title}")
                return redirect('dashboard')
            else:
                print("Normal form errors:", normal_task_form.errors)

        elif task_type == 'continuous':
            continuous_task_form = ContinuousTaskForm(request.POST)
            if continuous_task_form.is_valid():
                continuous_task = continuous_task_form.save(commit=False)
                continuous_task.user = request.user
                continuous_task.save()
                print(f"Continuous task created: {continuous_task.title}")
                return redirect('dashboard')
            else:
                print("Continuous form errors:", continuous_task_form.errors)
            

    context = {
        'normal_tasks': normal_tasks,
        'continuous_tasks': continuous_tasks,
        'normal_task_form': normal_task_form,
        'continuous_task_form': continuous_task_form,
    }
    return render(request, 'tasks/dashboard.html', context)