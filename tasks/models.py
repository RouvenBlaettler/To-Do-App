from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def NormalTask():
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
def ContinuousTask():
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work_time = models.PositiveIntegerField(default=0)  # in hours
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    on_going = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    