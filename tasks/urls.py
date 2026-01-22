from django.contrib import admin
from django.urls import path
from .views import dashboard, register, login_view, logout_view, edit_task

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit_task/<int:task_id>/<str:task_type>/', edit_task, name='edit_task'),
]