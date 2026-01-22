from django.contrib import admin
from django.urls import path
from .views import dashboard, register, login_view

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
]