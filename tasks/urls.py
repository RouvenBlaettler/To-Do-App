from django.contrib import admin
from django.urls import path
from .views import dashboard, register, login_view, logout_view, edit_task, delete_task, dice_roll, complete_task, increment_work_time

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit_task/<int:task_id>/<str:task_type>/', edit_task, name='edit_task'),
    path('delete_task/<int:task_id>/<str:task_type>/', delete_task, name='delete_task'),
    path('dice_roll/', dice_roll, name='dice_roll'),
    path('complete_task/<int:task_id>/<str:task_type>/', complete_task, name='complete_task'),
    path('increment_work_time/<int:task_id>/', increment_work_time, name='increment_work_time'),
]