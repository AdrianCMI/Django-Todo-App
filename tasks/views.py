from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, 'home.html')



def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe...'
                })
            return redirect(tasks)
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden...'
        })
    else:
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })


@login_required
def tasks(request):
    return render(request, 'tasks.html', {
        'tasks': Task.objects.filter(user=request.user, complete=False).order_by('created')
    })


@login_required
def logout_view(request):
    logout(request)
    return redirect(home)



def signin(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Credenciales incorrectas...'
            })
        login(request, user)
        return redirect(tasks)
    return render(request, 'signin.html', {
        'form': AuthenticationForm
    })
    
    
@login_required
def create_task(request):
    if request.method == 'POST':
        try:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                return redirect(tasks)
        except Exception as e:
            return render(request, 'create_task.html', {
                'form': TaskForm(),
                'error': 'Error al crear la tarea: {}'.format(e)
            })
    return render(request, 'create_task.html', {
        'form': TaskForm
    })
    
    
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        try:
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect(tasks)
        except Exception as e:
            return render(request, 'task_detail.html', {
                'task': task,
                'form' : TaskForm(instance=task),
                'error': 'Error al actualizar la tarea: {}'.format(e)
            })
    return render(request, 'task_detail.html', {
        'task': task,
        'form' : TaskForm(instance=task)
    })
    
    
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.complete = True
        task.save()
        return redirect(tasks)
    
    
@login_required   
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect(tasks)
    
    
@login_required    
def completed(request):
    return render(request, 'completed.html', {
        'tasks': Task.objects.filter(user=request.user, complete=True).order_by('created')
    })