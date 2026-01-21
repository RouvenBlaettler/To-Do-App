from django.contrib import admin
from django.urls import path
from .views import task_list

urlpatterns = [
    path('', task_list),
]