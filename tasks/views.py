from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
#**************************************************************************
def home(req):
  return render(req, 'home.html')
#**************************************************************************
def signup(req):
  if req.method == 'GET':
    return render(req, 'signup.html',{
    'form': UserCreationForm
  })
  else:
    if req.POST['password1'] == req.POST['password2']:
      try:
        user = User.objects.create_user(username=req.POST['username'],
        password=req.POST['password1'])
        user.save()
        login(req, user)
        return redirect('tasks')
      except IntegrityError:
        return render(req, 'signup.html',{
          'form':UserCreationForm,
          'error':'Username already exists'
        })
    return render(req, 'signup.html',{
      'form':UserCreationForm,
      'error':'Password to not match'
    })
#**************************************************************************
@login_required
def tasks(req):
  tasks = Task.objects.filter(user=req.user, datecompleted__isnull=True)
  return render(req, 'tasks.html', {'tasks':tasks})
#**************************************************************************
@login_required
def tasksCompleted(req):
  tasks = Task.objects.filter(user=req.user, datecompleted__isnull=False).order_by('-datecompleted')
  return render(req, 'tasks.html', {'tasks':tasks})
#**************************************************************************
@login_required
def createTask(req):
  if req.method == 'GET':
    return render(req, 'create_task.html',{
      'form': TaskForm
    })
  else:
    try:
      form = TaskForm(req.POST)
      new_task = form.save(commit=False) 
      new_task.user = req.user
      new_task.save()

      return redirect('tasks')
    except ValueError:
      return render(req, 'create_task.html',{
      'form':TaskForm,
      'error':'Please provide valida data'
    })
#**************************************************************************
@login_required
def taskDetail(req, task_id):
  if req.method == 'GET':
    task = get_object_or_404(Task, pk=task_id, user=req.user)
    form = TaskForm(instance=task)
    return render(req, 'task_detail.html', {'task':task, 'form':form})
  else:
    try:
      task = get_object_or_404(Task, pk=task_id, user=req.user)
      form = TaskForm(req.POST, instance=task)
      form.save()
      return redirect('tasks')
    except ValueError:
      return render(req, 'task_detail.html', {
        'task':task, 
        'form':form,
        'error':'Error updating task'
        })
      
#**************************************************************************
@login_required
def completeTask(req, task_id):
  task = get_object_or_404(Task, pk=task_id, user=req.user)
  if req.method == 'POST':
    task.datecompleted = timezone.now()
    task.save()
    return redirect('tasks')
#**************************************************************************
@login_required
def deleteTask(req, task_id):
  task = get_object_or_404(Task, pk=task_id, user=req.user)
  if req.method == 'POST':
    task.datecompleted = timezone.now()
    task.delete()
    return redirect('tasks')

#**************************************************************************
@login_required
def signout(req):
  logout(req)
  return redirect('home')
#**************************************************************************
def signin(req):
  if req.method == 'GET':
      return render(req, 'signin.html',{
      'form':AuthenticationForm
    })
  else:
      user = authenticate(
          req, username=req.POST['username'],
          password=req.POST['password']
        ) 
      if user is None:
        return render(req, 'signin.html',{
        'form':AuthenticationForm,
        'error': 'Username or password is incorrect'
      })
      else:
        login(req, user)
        return redirect('tasks')
#**************************************************************************









