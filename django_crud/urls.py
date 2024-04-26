"""
URL configuration for django_crud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
path('admin/', admin.site.urls),
path('', views.home, name='home'),
path('signup/', views.signup, name='signup'),
path('tasks/', views.tasks, name='tasks'),
path('tasks_completed/', views.tasksCompleted, name='tasks_completed'),
path('tasks/create/', views.createTask, name='create_task'),
path('tasks/<int:task_id>/', views.taskDetail, name='task_detail'),
path('tasks/<int:task_id>/complete', views.completeTask, name='complete_task'),  
path('tasks/<int:task_id>/delete', views.deleteTask, name='delete_task'),  
path('logout/', views.signout, name='logout'),
path('signin/', views.signin, name='signin'),
]
