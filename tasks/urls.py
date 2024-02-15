from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('completed', views.completed, name='completed'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    
]

